from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from .models import *
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from .forms import NewsForm
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

def home(request):
    news = News.objects.all()
    return render(request=request, template_name="index.html", context={"news": news})


class CreateNews(CreateView):
    form_class = NewsForm
    success_url = reverse_lazy("home")
    template_name = "create_news.html"

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, "Your new post has been completed.")
        return super().form_valid(form)


def about(request):
    team = Team.objects.all()
    return render(request=request, template_name="about.html", context={"team": team}) 


class MyNews(ListView):
    model = News
    context_object_name = "news"

    def get_queryset(self) -> QuerySet[Any]:
        queryset = super(MyNews, self).get_queryset()
        queryset = queryset.filter(user=self.request.user)
        return queryset


class MyNewsDetail(LoginRequiredMixin, DetailView):
    model = News
    context_object_name = "news"

    def get_queryset(self):
        queryset = super(MyNewsDetail, self).get_queryset()
        queryset = queryset.filter(user=self.request.user)
        return queryset


class MyNewsUpdate(LoginRequiredMixin, UpdateView):
    model = News
    context_object_name = "news"
    form_class = NewsForm
    success_url = reverse_lazy("my_news")

    def get_queryset(self):
        queryset = super(MyNewsUpdate, self).get_queryset()
        queryset = queryset.filter(user=self.request.user)
        return queryset

    def form_valid(self, form):
        messages.success(self.request, "News instance is updated!")
        return super().form_valid(form)


class MyNewsDelete(LoginRequiredMixin, DeleteView):
    model = News
    context_object_name = "news"
    success_url = reverse_lazy("my_news")

    def get_queryset(self):
        queryset = super(MyNewsDelete, self).get_queryset()
        queryset = queryset.filter(user=self.request.user)
        return queryset

    def form_valid(self, form):
        messages.info(self.request, "News instance is deleted!")
        return super().form_valid(form)
