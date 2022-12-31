from rest_framework import serializers
from easy_food.models import Food


class EasyFoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields = "__all__"

