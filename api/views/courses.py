from rest_framework.viewsets import ReadOnlyModelViewSet

from api import models
from api.serializers import CourseSerializer


class CourseViewSet(ReadOnlyModelViewSet):
    """
    课程相关API视图
    """
    queryset = models.Course.objects.all()
    serializer_class = CourseSerializer
