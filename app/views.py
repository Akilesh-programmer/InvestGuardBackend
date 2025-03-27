from django.shortcuts import render
from django.http import HttpResponse
from .models import UserModel , Stock , InvestModel , UserCompany
from .serializer import UserSerializer, LoginSerializer , StockSerializer , InvestModelSerializer , ListUserSerializer
from rest_framework import generics, status
from django.contrib.auth.models import User , Permission
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.contrib.contenttypes.models import ContentType

# Create your views here.
def hello(request):
    return HttpResponse("Hello")
#Register
class Register(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        models = [Stock,InvestModel]
        for model in models:
            content_type = ContentType.objects.get_for_model(model)
            permissions = Permission.objects.filter(content_type=content_type)
            user.user_permissions.add(*permissions)
        user.save()
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
    # queryset = Stock.objects.all()
    serializer_class = StockSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Stock.objects.filter(investmodel__user = self.request.user)

class InvestModelCreateView(generics.ListCreateAPIView):
    # queryset = InvestModel.objects.all()
    serializer_class = InvestModelSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return InvestModel.objects.filter(user = self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class SeeUsersView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = ListUserSerializer


class DestroyUserView(generics.DestroyAPIView):
    queryset = User.objects.all()
    lookup_field = 'id'


class DeleteInvestmentView(generics.DestroyAPIView):
    queryset = InvestModel.objects.all()
    lookup_field = 'id'







