from django.shortcuts import render
from django.http import HttpResponse
from .models import UserModel , Stock , InvestModel , UserCompany
from .serializer import UserSerializer, LoginSerializer , StockSerializer , InvestModelSerializer , ListUserSerializer
from rest_framework import generics, status
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

# Create your views here.
def hello(request):
    return HttpResponse("Hello")
#Register
class Register(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
#Login
class Login(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]
    def post(self,request):
        serializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        username = serializer.validated_data["username"]
        password  = serializer.validated_data["password"]
        user = authenticate(username = username,password=password)
        if user:
            token , created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key},status=status.HTTP_200_OK)
        return Response({"error": "Invalid credentials"},status = status.HTTP_401_UNAUTHORIZED)
    
class StockViewSet(generics.ListCreateAPIView):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer

class InvestModelCreateView(generics.ListCreateAPIView):
    queryset = InvestModel.objects.all()
    serializer_class = InvestModelSerializer

class SeeUsersView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = ListUserSerializer


class DestroyUserView(generics.DestroyAPIView):
    queryset = User.objects.all()
    lookup_field = 'id'


class DeleteInvestmentView(generics.DestroyAPIView):
    queryset = InvestModel.objects.all()
    lookup_field = 'id'







