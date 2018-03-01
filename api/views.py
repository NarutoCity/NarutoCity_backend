import json, time, hashlib
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView

from api import models
from api.serializers import courses, articles


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

        return Response(ret)


class CourseViewSet(ReadOnlyModelViewSet):
    """
    课程相关API视图
    """
    queryset = models.Course.objects.all()
    serializer_class = courses.CourseSerializer


class ArticleViewSet(ReadOnlyModelViewSet):
    """
    文章相关API视图
    """
    queryset = models.Article.objects.all()
    serializer_class = articles.ArticleSerializer

# class ArticlesView(APIView):
#     """深科技展示页"""
#
#     def get(self, request, *args, **kwargs):
#         ret = {"error_no": 0, "data": {"count": None, "next": None, "previous": None, "results": []}}
#         articles = models.Article.objects.all()
#         ret['data']['count'] = articles.count()
#         for article in articles:
#             temp = {}
#             temp["id"] = article.id
#             temp["title"] = article.title
#             temp["brief"] = article.brief
#             temp["date"] = "2小时前"
#             temp["article_type"] = article.article_type
#             temp["collect_num"] = article.collect_num
#             temp["view_num"] = article.view_num
#             temp["head_img"] = article.head_img
#             temp["comment_num"] = article.comment_num
#
#             ret['data']['results'].append(temp)
#         return Response(ret)
#
#
# class ArticleView(APIView):
#     """深科技详细页"""
#
#     def get(self, request, *args, **kwargs):
#         ret = {"error_no": 0, "data": {}}
#         pk = kwargs.get('pk')
#         article = models.Article.objects.get(id=pk)
#         ret_data = ret["data"]
#
#         ret_data["id"] = article.id
#         ret_data["title"] = article.title
#         ret_data["brief"] = article.brief
#         ret_data["date"] = "2小时前"
#         ret_data["article_type"] = article.article_type
#         ret_data["collect_num"] = article.collect_num
#         ret_data["view_num"] = article.view_num
#         ret_data["head_img"] = article.head_img
#         ret_data["comment_num"] = article.comment_num
#         ret_data["content"] = article.content
#         ret_data["up_num"] = article.agree_num
#         return Response(ret)
#
#
# class Courses(APIView):
#     def get(self, request, *args, **kwargs):
#         courseList = models.Course.objects.all()
#         ret = course_serializer.CourseSerializer(instance=courseList, many=True)
#         return Response(ret.data)
#
#
# class CourseDetail(APIView):
#     def get(self, request, *args, **kwargs):
#         # 根据请求课程id判断返回数据
#         courseItem = models.Course.objects.filter(id=pk).first()
#         # 序列化数据
#         ret = course_serializer.CourseSerializer(instance=courseItem)
#         return Response(ret.data)
