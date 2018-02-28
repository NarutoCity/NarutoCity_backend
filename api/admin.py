from django.contrib import admin
from api import models

# Register your models here.
admin.register(models.Article)
admin.register(models.ArticleSource)
admin.register(models.Collection)
admin.register(models.Comment)