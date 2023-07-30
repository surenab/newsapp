from django.contrib import admin
from django.urls import path, include
from .views import Register, home, home2

urlpatterns = [
    path('', include("django.contrib.auth.urls")),
    path('register/', Register.as_view(), name = "register"),
    path('home/', home, name = "home"),
    path('home2/', home2, name = "home2"),
]
