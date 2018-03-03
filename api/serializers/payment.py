from rest_framework import serializers

from api.models import Course


class ShoppingCartSerializer(serializers.ModelSerializer):
    price_policy_list = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ['name', 'course_img', 'price_policy_list']

    def get_price_policy_list(self, obj):
        ret = []
        for item in obj.price_policy.all():
            ret.append({'id': item.id, 'valid_period': item.get_valid_period_display(), 'price': item.price})

        return ret
