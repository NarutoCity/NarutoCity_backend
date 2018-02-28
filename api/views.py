from django.shortcuts import render

from rest_framework import renderers
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import detail_route
from rest_framework import permissions
from rest_framework.views import APIView
from api import models
from django.http import JsonResponse


class ArticlesView(APIView):
    """深科技展示页"""
    def get(self, request, *args, **kwargs):
        ret = {"error_no": 0, "data": {"count": None, "next": None, "previous": None, "results":[]}}
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