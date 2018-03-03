from rest_framework.viewsets import ReadOnlyModelViewSet

from api import models
from api.serializers import ArticleSerializer


class ArticleViewSet(ReadOnlyModelViewSet):
    """
    文章相关API视图
    """
    queryset = models.Article.objects.all()
    serializer_class = ArticleSerializer
