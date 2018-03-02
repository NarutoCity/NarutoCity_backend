import json, datetime, time, hashlib,redis
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import renderers
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import detail_route
from rest_framework import permissions
from rest_framework.exceptions import APIException
from rest_framework.authentication import BaseAuthentication
from rest_framework.views import APIView
from api import models
from rest_framework.parsers import JSONParser
from django.core.exceptions import ObjectDoesNotExist

class PricePolicyDoesNotExist(Exception):
    pass

CONN=redis.Redis(host="192.168.20.145")



class LoginView(APIView):
    def post(self, request):
        json_content = json.loads(request.body)
        username = json_content.get("username")
        pwd = json_content.get("password")
        user = models.Account.objects.filter(username=username, password=pwd).first()
        if user:
            ctime = time.time()
            key = "%s|%s" % (username, ctime)
            m = hashlib.md5()
            m.update(key.encode("utf-8"))
            token = m.hexdigest()
            obj = models.UserAuthToken.objects.filter(user=user).first()
            if not obj:
                models.UserAuthToken.objects.create(token=token, user=user)
            else:
                models.UserAuthToken.objects.update(token=token)
            ret = {
                'status': 1000,
                'username': username,
                'token': token
            }
        else:
            ret = {
                'status': 1001,
                'msg': "用户名或者密码错误"
            }

        return JsonResponse(ret)


class ArticlesView(APIView):
    """深科技展示页"""

    def get(self, request, *args, **kwargs):
        ret = {"error_no": 0, "data": {"count": None, "next": None, "previous": None, "results": []}}
        articles = models.Article.objects.all()
        ret['data']['count'] = articles.count()
        for article in articles:
            temp = {}
            temp["id"] = article.id
            temp["title"] = article.title
            temp["brief"] = article.brief
            temp["date"] = "2小时前"
            temp["article_type"] = article.article_type
            temp["collect_num"] = article.collect_num
            temp["view_num"] = article.view_num
            temp["head_img"] = article.head_img
            temp["comment_num"] = article.comment_num
            ret['data']['results'].append(temp)
        return JsonResponse(ret, json_dumps_params={"ensure_ascii": False})


class ArticleView(APIView):
    """深科技详细页"""

    def get(self, request, *args, **kwargs):
        ret = {"error_no": 0, "data": {}}
        nid = kwargs.get('nid')
        article = models.Article.objects.get(id=nid)
        ret["data"]["id"] = article.id
        ret["data"]["title"] = article.title
        ret["data"]["brief"] = article.brief
        ret["data"]["date"] = "2小时前"
        ret["data"]["article_type"] = article.article_type
        ret["data"]["collect_num"] = article.collect_num
        ret["data"]["view_num"] = article.view_num
        ret["data"]["head_img"] = article.head_img
        ret["data"]["comment_num"] = article.comment_num
        ret["data"]["content"] = article.content
        ret["data"]["up_num"] = article.agree_num
        return JsonResponse(ret, json_dumps_params={"ensure_ascii": False})

class MyAuthenticate(BaseAuthentication):
    def authenticate(self, request):
        token=request.query_params.get("token")
        obj=models.UserAuthToken.objects.filter(token=token).first()
        if obj:
            return (obj.user.username,obj.user)
        raise APIException("用户认证失败")

class ShoppingCarView(APIView):

    authentication_classes = [MyAuthenticate,]

    def get(self,request,*args,**kwargs):
        course=CONN.hget("luffy_shopping_car",request.auth.id)
        course_dict=json.loads(course.decode("utf-8"))
        return Response(course_dict)

    def post(self,request,*args,**kwargs):
        """
        需要请求数据:课程id,策略id,放入redis
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        ret={"code":1000,"msg":None}
        try:
            course_id=request.data.get("course_id")
            price_policy_id=request.data.get("price_policy_id")
            course_obj=models.Course.objects.get(id=course_id)
            price_policy_list=[]
            flag=True
            price_policy_obj_list=course_obj.price_policy.all()
            for item in price_policy_obj_list:
                if item.id==price_policy_id:
                    flag=False
                price_policy_list.append({"id":item.id,"valid_period":item.get_valid_period_display(),"price":item.price})
            if flag:
                raise PricePolicyDoesNotExist()

            course_dict={
                "id":course_obj.id,
                "img":course_obj.course_img,
                "title":course_obj.name,
                "price_policy_list":price_policy_list,
                "default_policy_id":price_policy_id
            }
            nothing=CONN.hget("luffy_shopping_car",request.auth.id)
            if not nothing:
                data={course_obj.id:course_dict}
            else:
                data=json.loads(nothing.decode("utf-8"))
                data[course_obj.id]=course_dict
            CONN.hset("luffy_shopping_car",request.auth.id,json.dumps(data))

        except ObjectDoesNotExist as e:
            ret["code"]=1001
            ret["msg"]="课程不存在"

        except PricePolicyDoesNotExist as e :
            ret["code"]=1002
            ret["msg"]="价格策略不存在"

        # except Exception as e:
        #     ret["code"]=1003
        #     ret["msg"]="添加购物车异常"
        return Response(ret)
