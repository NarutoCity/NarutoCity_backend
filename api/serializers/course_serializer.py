from rest_framework import serializers
from api.models import Course


class CourseChapterCharField(serializers.CharField):
    """章节"""

    def to_representation(self, instance):
        """
        :param instance:QuerySet对象
        """
        data_list = []
        for row in instance:
            data_list.append({'price': row.price, 'valid_period': row.get_valid_period_display()})
        return data_list


class QuestionCharField(serializers.CharField):
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
        fields = ['id', 'name', 'course_img', 'brief', 'level', 'course_type', 'pub_date', 'period', 'order',
                  'attachment_path', 'status', 'template_id', 'sub_category',
                  'hours', 'why_study', 'what_to_study_brief', 'career_improvement', 'prerequisite',
                  'recommend_courses', 'teachers', 'price_policy', 'questions',
                  ]

    level = serializers.SerializerMethodField()
    course_type = serializers.SerializerMethodField()
    hours = serializers.CharField(source="coursedetail.hours")
    why_study = serializers.CharField(source="coursedetail.why_study")
    what_to_study_brief = serializers.CharField(source="coursedetail.career_improvement")
    career_improvement = serializers.CharField(source="coursedetail.career_improvement")
    prerequisite = serializers.CharField(source="coursedetail.prerequisite")

    recommend_courses = serializers.SerializerMethodField()
    teachers = serializers.SerializerMethodField()
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
