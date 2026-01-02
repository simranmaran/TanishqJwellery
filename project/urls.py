from django.urls import path
from app import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('registerdata/', views.registerdata, name='registerdata'),
    path('login/', views.login, name='login'),
    path('logindata/', views.logindata, name='logindata'),
    path('dashboard/', views.dashboard, name='dashboard'),
]
