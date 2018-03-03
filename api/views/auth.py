import json
from rest_framework.views import APIView
from rest_framework.response import Response

from api import models


class LoginView(APIView):
    """
    登录校验
    """

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = models.Account.objects.filter(username=username, password=password).first()
        if user:
            import time, hashlib
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

            ret = {'status': True, 'username': username, 'token': token}
        else:
            ret = {'status': False, 'msg': "用户名或者密码错误"}

        return Response(ret)
