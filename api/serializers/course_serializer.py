from rest_framework import serializers
from rest_framework.serializers import CharField, SerializerMethodField
from api.models import Course


class CourseChapterCharField(CharField):
    """章节"""

    def to_representation(self, instance):
        """
        :param instance:QuerySet对象
        """
        data_list = []
        for row in instance:
            data_list.append({'price': row.price, 'valid_period': row.get_valid_period_display()})
        return data_list


class QuestionCharField(CharField):
    """问题"""

    def to_representation(self, instance):
        """
        :param instance:QuerySet对象
        """
        data_list = []
        for row in instance:
            data_list.append({'question': row.question, 'answer': row.answer})
        return data_list


class CourseSerializer(serializers.ModelSerializer):
    """获取一条记录对象"""

    class Meta:
        model = Course
        fields = '__all__'

    level = SerializerMethodField()
    course_type = SerializerMethodField()
    video_brief_link = CharField(source="coursedetail.video_brief_link")
    hours = CharField(source="coursedetail.hours")

    course_slogan = CharField(source="coursedetail.course_slogan")
    why_study = CharField(source="coursedetail.why_study")
    what_to_study_brief = CharField(source="coursedetail.what_to_study_brief")
    career_improvement = CharField(source="coursedetail.career_improvement")
    recommend_courses = SerializerMethodField()
    prerequisite = CharField(source="coursedetail.prerequisite")
    teachers = SerializerMethodField()
    price_policy = CourseChapterCharField(source="price_policy.all")
    questions = QuestionCharField(source="questions.all")

    def get_level(self, obj):
        """课程难度级别"""
        return obj.get_level_display()

    def get_course_type(self, obj):
        """课程类型"""
        return obj.get_course_type_display()

    def get_recommend_courses(self, obj):
        """推荐课程"""
        return obj.coursedetail.recommend_courses.values('id', 'name')

    def get_teachers(self, obj):
        """讲师"""
        return obj.coursedetail.teachers.values('name', 'role', 'image', 'signature')
