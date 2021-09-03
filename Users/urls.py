from django.contrib import admin
from django.urls import path
from Users.views import *

urlpatterns = [
    path('signup', SignupView.as_view(), name='signup'),
    path('login', LoginView.as_view(), name='login'),
    path('users', UserView.as_view(), name='users'),
    path('users/<int:pk>', DelView.as_view(), name='deleteuser'),
    path('logout', LogoutView.as_view(), name='logout'),
]
