from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^login$', views.Login.as_view()),
    url(r'^courses/', views.Courses.as_view()),
    url(r'^coursedetail/(?P<pk>\d+)/', views.CourseDetail.as_view()),
]
