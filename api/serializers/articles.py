from rest_framework import serializers
from rest_framework.serializers import CharField, SerializerMethodField
from api.models import Article


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'

    article_type = SerializerMethodField()
    status = SerializerMethodField()
    position = SerializerMethodField()
    source = CharField(source="source.name")

    def get_article_type(self, obj):
        """文章类型"""
        return obj.get_article_type_display()

    def get_status(self, obj):
        """文章在线情况"""
        return obj.get_status_display()

    def get_position(self, obj):
        """文章配图设置"""
        return obj.get_position_display()

# 还需要添加的数据：
# 评论数、上线时间（2小时前）
