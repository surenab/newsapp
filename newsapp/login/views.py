from django.shortcuts import render
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import RegisterForm
from django.http import HttpResponse


# Create your views here.

class Register(CreateView):
    form_class = RegisterForm
    success_url = reverse_lazy("login")
    template_name = "registration/register.html"


def home(request):
    return HttpResponse(f"Home page for {request.user.username}")


def home2(request):
    return HttpResponse("Home page after logout: NO user info")
