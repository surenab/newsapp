from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from .models import *
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from .forms import NewsForm, MessageForm
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django_filters.views import FilterView
from .filters import NewsFilter
from django_filters.views import FilterView
from .models import News



# Create your views here.

def home(request):
    news = News.objects.all()
    return render(request=request, template_name="index.html", context={"news": news})


def profile(request):
    news = News.objects.all()
    return render(request=request, template_name="core/profile.html", context={"news": news})


def about(request):
    team = Team.objects.all()
    return render(request=request, template_name="about.html", context={"team": team}) 


class Base(LoginRequiredMixin):
    def get_queryset(self):
        queryset = super(Base, self).get_queryset()
        queryset = queryset.filter(user=self.request.user)
        return queryset


class NewsBase(Base):
    model = News
    context_object_name = "news"
    form_class = NewsForm
    success_url = reverse_lazy("my_news")
    success_text = ""
    
    def form_valid(self, form):
        messages.success(self.request, self.success_text)
        return super().form_valid(form)


class CreateNews(NewsBase, CreateView):
    template_name = "create_news.html"

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, "Your new post has been completed.")
        return super().form_valid(form)


class MyNews(NewsBase, FilterView):
    template_name = "core/news_list.html"
    filterset_class = NewsFilter
    paginate_by = 2


class MyNewsDetail(NewsBase, DetailView):
    pass


class MyNewsUpdate(NewsBase, UpdateView):
    success_text = "News instance is updated!"


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



def search(request):
    news = News.objects.all()
    return render(request, "search-result.html", context={"news": news})

def single_post(request):
    news = News.objects.all()
    return render(request, "single-post.html", context={"news": news})

def contact(request):
    status = 200

    if request.method == "POST":
        print("POSTED DATA")
        print(request.POST)
        form = MessageForm(request.POST)
        if form.is_valid():
            form.save()
            status = 201
        else:
            print("TELL them that sent data is not valid")
    messageForm = MessageForm()
    return render(request=request, template_name="contact.html", context= {"messageForm": messageForm}, status=status)


class Filter(NewsBase, FilterView):
    template_name = "core/all_news.html"
    filterset_class = NewsFilter
    paginate_by = 3


def category(request):
    news = News.objects.all()
    return render(request, "category.html", context={"news": news})
