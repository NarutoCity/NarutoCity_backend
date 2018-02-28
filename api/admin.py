from django.contrib import admin

from api import models
from .models import *

admin.site.register(
    [CourseSubCategory, CourseCategory, Course, CourseDetail, DegreeCourse, Scholarship, OftenAskedQuestion,
     CourseOutline, CourseChapter, CourseSection, PricePolicy, Coupon, Teacher, ArticleSource, Article, Collection,
     Comment, Account, UserAuthToken])

admin.site.register(models.Article)
admin.site.register(models.ArticleSource)
admin.site.register(models.Collection)
admin.site.register(models.Comment)
