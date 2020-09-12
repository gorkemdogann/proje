from django.urls import path
from .views import *
from . import views


urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='user_login'),
    path('logout/', views.user_logout, name='user_logout'),
    path('?P<username>/', views.user_profile, name='user_profile'),

]