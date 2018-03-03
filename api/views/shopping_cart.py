"""
说明：
    注释为# -=-=的地方，需要把数字1改为request.user.id
"""

import json

from rest_framework.views import APIView
from rest_framework.response import Response

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

from api.models import Course
from api.serializers import ShoppingCartSerializer
from api.utils import redis_pool
from api.utils.exceptions import PricePolicyDoesNotExist

CONN = redis_pool.conn


class ShoppingCartView(APIView):
    authentication_classes = []  # 这里应该有UserToken验证
    permission_classes = []

    def post(self, request):
        """添加课程到购物车"""

        res = {'status': 100, 'msg': None}
        try:
            course_id = str(request.data.get('course_id'))
            policy_id = str(request.data.get('policy_id'))

            course_obj = Course.objects.filter(status=0).get(id=course_id)
            serializer = ShoppingCartSerializer(course_obj, many=False)
            course_info_dict = serializer.data

            # 判断前端获取的价格策略是否存在，防止恶意修改
            policy_exist = False
            for policy in course_info_dict.get('price_policy_list'):
                if policy.get('id') == policy_id or str(policy.get('id')) == policy_id:
                    policy_exist = True
                    break
            if not policy_exist:
                raise PricePolicyDoesNotExist('价格策略不存在')

            # 把选中的价格策略的id添加到course_info_dict中
            course_info_dict.setdefault('chosen_policy_id', policy_id)

            # 获取Redis中当前用户的购物车信息，如果没有当前课程则添加，否则更新
            user_cart = CONN.hget(settings.REDIS_SHOPPING_CAR_KEY, 1)  # -=-=
            if not user_cart:
                user_cart = {course_id: course_info_dict}
                res['msg'] = '课程添加成功'
            else:
                user_cart = json.loads(user_cart.decode('utf8'))  # type:dict
                user_cart.update({course_id: course_info_dict})
                res['msg'] = '购物车更新'

            CONN.hset(settings.REDIS_SHOPPING_CAR_KEY, 1, json.dumps(user_cart))  # -=-=
            # print(json.loads(CONN.hget(settings.REDIS_SHOPPING_CAR_KEY, 1).decode('utf8')))  # -=-=

        except ObjectDoesNotExist:
            res['status'] = 201
            res['msg'] = '课程不存在'
        except PricePolicyDoesNotExist:
            res['status'] = 202
            res['msg'] = '价格策略不存在'
        except Exception as e:
            print(e)
            res['status'] = 200
            res['msg'] = str(e)

        return Response(res)

    def get(self, request):
        """根据用户id获取购物车中课程的信息"""

        res = {'status': 100, 'msg': '购物车为空', 'data': None}
        try:
            user_cart = CONN.hget(settings.REDIS_SHOPPING_CAR_KEY, 1)  # -=-=
            if user_cart:
                user_cart = json.loads(user_cart.decode('utf8'))  # type:dict
                res['msg'] = '购物车信息获取成功'
                res['data'] = user_cart

        except Exception as e:
            res['status'] = 200
            res['msg'] = str(e)

        return Response(res)

    def put(self, request):
        """更新购物车中课程的价格策略"""

        res = {'status': 100, 'msg': None}
        try:
            course_id = str(request.data.get('course_id'))
            policy_id = str(request.data.get('policy_id'))

            # 获取Redis中当前用户的购物车信息，如果其中有该课程则修改价格策略
            user_cart = CONN.hget(settings.REDIS_SHOPPING_CAR_KEY, 1)  # -=-=

            # 判断购物车是否为空
            if not user_cart:
                raise Exception('购物车为空')

            # 判断购物车中是否存在该课程，防止恶意修改
            user_cart = json.loads(user_cart.decode('utf8'))  # type:dict
            if course_id not in user_cart:
                raise Exception('购物车中没有该课程')

            # 判断前端获取的价格策略是否存在，防止恶意修改
            policy_exist = False
            for policy in user_cart.get(course_id).get('price_policy_list'):
                if policy.get('id') == policy_id or str(policy.get('id')) == policy_id:
                    policy_exist = True
                    break
            if not policy_exist:
                raise PricePolicyDoesNotExist('价格策略不存在')

            user_cart[course_id]['chosen_policy_id'] = policy_id
            CONN.hset(settings.REDIS_SHOPPING_CAR_KEY, 1, json.dumps(user_cart))  # -=-=
            res['msg'] = '购物车更新'
            print(json.loads(CONN.hget(settings.REDIS_SHOPPING_CAR_KEY, 1).decode('utf8')))  # -=-=

        except PricePolicyDoesNotExist:
            res['status'] = 201
            res['msg'] = '价格策略不存在'
        except Exception as e:
            res['status'] = 200
            res['msg'] = str(e)

        return Response(res)

    def delete(self, request):
        """从购物车删除课程"""

        res = {'status': 100, 'msg': None}
        try:
            course_id = str(request.data.get('course_id'))
            # 获取Redis中当前用户的购物车信息，如果其中有该课程则删除
            user_cart = CONN.hget(settings.REDIS_SHOPPING_CAR_KEY, 1)  # -=-=

            # 判断购物车是否为空
            if not user_cart:
                raise Exception('购物车为空')

            # 判断购物车中是否存在该课程，防止恶意修改
            user_cart = json.loads(user_cart.decode('utf8'))  # type:dict
            if course_id not in user_cart:
                raise Exception('购物车中没有该课程')

            user_cart.pop(course_id)

            CONN.hset(settings.REDIS_SHOPPING_CAR_KEY, 1, json.dumps(user_cart))  # -=-=
            res['status'] = '课程删除成功'
            # print(json.loads(CONN.hget(settings.REDIS_SHOPPING_CAR_KEY, 1).decode('utf8')))  # -=-=

        except Exception as e:
            res['status'] = 200
            res['msg'] = str(e)

        return Response(res)
