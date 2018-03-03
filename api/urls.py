from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from api import views

router = DefaultRouter()
router.register(r'courses', views.CourseViewSet)
router.register(r'articles', views.ArticleViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^shopping_cart/$', views.ShoppingCartView.as_view()),

    url(r'^login/', views.LoginView.as_view()),
]
