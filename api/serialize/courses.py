from rest_framework import serializers
from ..models import *


class CourseCapterCharField(serializers.CharField):
    """章节"""
    def to_representation(self, instance):
        # instance是QuerySet对象
        data_list = []
        for row in instance:
            data_list.append({'price': row.price, 'valid_period': row.get_valid_period_display()})
        return data_list


class QuestionCharField(serializers.CharField):
    """问题"""
    def to_representation(self, instance):
        # instance是QuerySet对象
        data_list = []
        for row in instance:
            data_list.append({'question': row.question, 'answer': row.answer})
        return data_list


class CourseSerializer(serializers.ModelSerializer):
    # 获取一个对象
    level = serializers.SerializerMethodField()
    course_type = serializers.SerializerMethodField()
    price_policy = CourseCapterCharField(source="price_policy.all")

    # 课程详细对象
    coursedetail = serializers.SerializerMethodField()

    # 推荐课程
    recommend_courses = serializers.SerializerMethodField()

    # 讲师
    teachers = serializers.SerializerMethodField()

    # 常见问题
    questions = QuestionCharField(source="questions.all")

    class Meta:
        model = Course
        fields = "__all__"
        depth = 2

    def get_level(self, obj):
        # 某个对象的钩子函数
        return obj.get_level_display()

    def get_course_type(self, obj):
        return obj.get_course_type_display()

    def get_coursedetail(self, obj):
        return {'hours': obj.coursedetail.hours, 'why_study': obj.coursedetail.why_study,
                'what_to_study_brief': obj.coursedetail.what_to_study_brief,
                'career_improvement': obj.coursedetail.career_improvement,
                'prerequisite': obj.coursedetail.prerequisite}

    def get_recommend_courses(self, obj):
        recommend_courses_list = obj.coursedetail.recommend_courses.all()
        data_list = []
        for item in recommend_courses_list:
            data_list.append({'name': item.name})
        return data_list

    def get_teachers(self, obj):
        recommend_courses_list = obj.coursedetail.teachers.all()
        data_list = []
        for item in recommend_courses_list:
            data_list.append({'name': item.name, 'role': item.get_role_display(),
                              'image': item.image, 'signature': item.signature, 'brief': item.brief})
        return data_list







