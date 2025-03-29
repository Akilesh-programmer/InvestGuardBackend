from django.urls import path
from . import views
urlpatterns = [
    path('',views.hello,name="hello"),
    path('users',views.SeeUsersView.as_view(),name="users"),
    path('register',views.Register.as_view(),name="register"),
    path('login',views.Login.as_view(),name="login"),
    path('stocks',views.StockViewSet.as_view(),name="stocks"),
    path('news',views.seeNews.as_view(),name="news"),
    path('users/<int:id>/delete',views.DestroyUserView.as_view(),name='delete'),
    path('investments',views.InvestModelCreateView.as_view(),name="investments"),
    path('investments/<int:id>/delete',views.DeleteInvestmentView.as_view(),name="investments"),
]
