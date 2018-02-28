from django.contrib import admin

from .models import *

admin.site.register(
    [CourseSubCategory, CourseCategory, Course, CourseDetail, DegreeCourse, Scholarship, OftenAskedQuestion,
     CourseOutline, CourseChapter, CourseSection, PricePolicy, Coupon, Teacher, CourseReview, DegreeCourseReview,
     ArticleSource, Article, Collection,
     Comment, Account, UserAuthToken])
