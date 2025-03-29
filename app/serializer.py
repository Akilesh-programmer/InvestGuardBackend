from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Stock , InvestModel , NewsHeadLines , ResponseModel

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
    def create(self,validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email = validated_data["email"],
            password = validated_data["password"]
        )
        user.is_staff = True
        user.save()
        return user
    

class ListUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username']

    
class LoginSerializer(serializers.Serializer):
    username= serializers.CharField()
    password = serializers.CharField(write_only = True)

class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = '__all__'

class InvestModelSerializer(serializers.ModelSerializer):
    total_price =  serializers.ReadOnlyField()
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = InvestModel
        fields = '__all__'


class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsHeadLines
        fields = '__all__'


class ResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResponseModel
        fields = '__all__'