import json,datetime,time,hashlib
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import renderers
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import detail_route
from rest_framework import permissions
from rest_framework.views import APIView
from api import models





class LoginView(APIView):
    def post(self,request):
        json_content=json.loads(request.body)
        username=json_content.get("username")
        pwd=json_content.get("password")
        user=models.Account.objects.filter(username=username,password=pwd).first()
        if user:
            ctime=time.time()
            key="%s|%s"%(username,ctime)
            m=hashlib.md5()
            m.update(key.encode("utf-8"))
            token=m.hexdigest()
            obj=models.UserAuthToken.objects.filter(user=user).first()
            if not obj:
                models.UserAuthToken.objects.create(token=token,user=user)
            else:
                models.UserAuthToken.objects.update(token=token)
            ret={
                'status':1000,
                'username':username,
                'token':token
            }
        else:
            ret={
                'status':1001,
                'msg':"用户名或者密码错误"
            }

        return JsonResponse(ret)
