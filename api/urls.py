from django.conf.urls import url
from django.contrib import admin
from api import views
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^articles/', views.ArticlesView.as_view()),
    url(r'^article/(?P<nid>\d+)/$', views.ArticleView.as_view()),
]
