from django.shortcuts import render
from rest_framework.viewsets import  ModelViewSet
from easy_food.models import Food
from easy_food.serializer import EasyFoodSerializer


class ShopAdminViewSet(ModelViewSet):
    serializer_class = EasyFoodSerializer
    queryset = Food.objects.all()

