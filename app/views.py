from django.shortcuts import render
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet
from app import models
from rest_framework import serializers
from drf_dynamic_fields import DynamicFieldsMixin



class get_sreializer(DynamicFieldsMixin,serializers.ModelSerializer):

    class Meta:
        model = models.Student
        fields = "__all__"



from app.pagination import MyCustomPagination

class MyChildCustomPagination(MyCustomPagination):

    page_size = 1 # 每页显示多少个

class get_view(mixins.CreateModelMixin,
               mixins.ListModelMixin,
               GenericViewSet):
    pagination_class = MyChildCustomPagination

    queryset = models.Student.objects.all()
    serializer_class = get_sreializer