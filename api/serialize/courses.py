from rest_framework import serializers
from ..models import *


class CourseSerializer(serializers.ModelSerializer):
    level = serializers.SerializerMethodField()  # 获取一个对象
    course_type = serializers.SerializerMethodField()

    # print(level)

    class Meta:
        model = Course
        fields = "__all__"
        depth = 2

    def get_level(self, obj):
        # 某个对象的钩子函数
        return obj.get_level_display()

    def get_course_type(self, obj):
        return obj.get_course_type_display()


class CourseCapterCharField(serializers.CharField):

    def to_representation(self, instance):
        # instance是QuerySet对象
        data_list = []
        for row in instance:
            for item in row.coursesections.all():
                data_list.append({'capter': row.chapter, 'sections': item.name})
        return data_list


class CourseDetailSerializer(serializers.ModelSerializer):

    level = serializers.SerializerMethodField()
    # course = serializers.SerializerMethodField()
    # 通过自定义的MyCharField中的to_representation处理多对多字段的QuerySet对象
    course_captal = CourseCapterCharField(source="course.coursechapters.all")

    class Meta:
        model = CourseDetail
        fields = "__all__"
        depth = 4

    def get_level(self, obj):
        # 该方法会在返回的json数据中添加一条数据,如果get_后面的名字和原始返回的数据重复则会覆盖原始的字段，如果不存在则会添加。
        # {'level': 'obj.course.get_level_display()',........}
        # {'id': 1, 'level': '中级',
        return obj.course.get_level_display()

    # def get_course(self, obj):
    #     # 覆盖了之前的course
    #     data = {}
    #     data['level'] = obj.course.get_level_display()
    #     return data


