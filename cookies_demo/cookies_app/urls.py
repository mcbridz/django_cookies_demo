from django.urls import path
from . import views

app_name = 'cookies_app'
urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('blowup/', views.blowup, name='blowup'),
    path('impossible/', views.impossible, name='impossible'),
]