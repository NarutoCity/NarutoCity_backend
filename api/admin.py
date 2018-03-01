from django.contrib import admin

from api.models import *

admin.site.register(
    [CourseSubCategory, CourseCategory, Course, CourseDetail, DegreeCourse, Scholarship, OftenAskedQuestion,
     CourseOutline, CourseChapter, CourseSection, PricePolicy, Coupon, Teacher, ArticleSource, Article, Collection,
     Comment, Account, UserAuthToken])
