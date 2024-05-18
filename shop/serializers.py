from rest_framework import serializers
from .models import Product
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

class OrderItemSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    quantity = serializers.IntegerField()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']

class ProductSerializer(serializers.ModelSerializer):
    user=UserSerializer()
    class Meta:
        model=Product
        fields="__all__"

class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['username','password']
        extra_kwargs={'password':{'write_only':True}}

    def create(self,validated_data):
        validated_data['password']=make_password(validated_data['password'])
        return super().create(validated_data)
    

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
