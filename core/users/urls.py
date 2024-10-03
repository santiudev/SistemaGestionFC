from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('test/', views.home, name='home'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
]
