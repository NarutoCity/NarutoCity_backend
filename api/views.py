from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from api import models

from .serialize import courses


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
        # print("====",courseList)
        ret = courses.CourseSerializer(instance=courseList, many=True)
        print(ret.data)
        return Response(ret.data)


class CourseDetail(APIView):
    def get(self, request, *args, **kwargs):
        # 根据请求课程id判断返回数据
        pk = kwargs.get('pk')
        if pk:
            courseDetail = models.CourseDetail.objects.get(id=pk)
            print(type(courseDetail))
            ret = courses.CourseDetailSerializer(instance=courseDetail)
            print(ret.data)
            return Response(ret.data)
