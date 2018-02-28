import json, datetime, time, hashlib
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from api import models

from .serializers import courses


class Login(APIView):
    def get(self, request, *args, **kwargs):
        return Response('login')

    def post(self, request):
        username = request.data['username']
        password = request.data['password']
        print(username, password)
        if username == '123' and password == '123':
            return Response('登录成功')
        return Response('用户名或密码错误')


class Courses(APIView):
    def get(self, request, *args, **kwargs):
        courseList = models.Course.objects.all()
        ret = courses.CourseSerializer(instance=courseList, many=True)
        return Response(ret.data)


class CourseDetail(APIView):
    def get(self, request, *args, **kwargs):
        # 根据请求课程id判断返回数据
        pk = kwargs.get('pk')
        if pk:
            courseItem = models.Course.objects.filter(id=pk).first()
            # 序列化数据
            ret = courses.CourseSerializer(instance=courseItem)
            return Response(ret.data)


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
