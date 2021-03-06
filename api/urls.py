"""narutocity_backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from api import views

router = DefaultRouter()
router.register(r'courses', views.CourseViewSet)
router.register(r'articles', views.ArticleViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),

    url(r'^login/', views.LoginView.as_view()),

    # url(r'^articles/$', views.ArticlesView.as_view()),
    # url(r'^article/(?P<pk>\d+)/$', views.ArticleView.as_view()),
    # url(r'^courses/$', views.Course.as_view()),
    # url(r'^coursedetail/(?P<pk>\d+)/$', views.CourseDetail.as_view()),

]
