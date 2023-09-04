from typing import Any, Dict
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect
from .models import *
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from .forms import NewsForm, MessageForm, NewsCommentForm
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django_filters.views import FilterView
from .filters import NewsFilter
from django_filters.views import FilterView
from .models import News, NewsComment
from django.http import HttpResponse, HttpRequest




# Create your views here.

# def home(request):
#     news = News.objects.all()
#     return render(request=request, template_name="index.html", context={"news": news})


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


class CreateNewsComment(CreateView):
    model = NewsComment
    form_class = NewsCommentForm
    # success_url = reverse_lazy("my_news")
    success_text = "Successfully created!"

    def get_success_url(self) -> str:
        return reverse_lazy("news_detail", kwargs = {"pk": self.request.POST.get("news")})

    def form_valid(self, form):
        form.instance.owner = self.request.user
        news_id = self.request.POST.get("news")
        news = News.objects.get(id = news_id)
        form.instance.news = news
        
        messages.success(self.request, "News Comment instance is created.")
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
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        data = super().get_context_data(**kwargs)
        data["comment_form"] = NewsCommentForm
        data["comments"] = NewsComment.objects.filter(news=data["news"])
        return data

class NewsDetails(DetailView):
    model = News
    template_name = "news-detail.html"
    context_object_name = "news"

    def get(self, request: HttpRequest, *args, **kwargs):
        self.object = self.get_object()
        self.object.view_count += 1
        self.object.save()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['comment_form'] = NewsCommentForm
        data['comments'] = NewsComment.objects.filter(news=data["news"])
        return data


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

# def contact(request):
#     status = 200

#     if request.method == "POST":
#         print("POSTED DATA")
#         print(request.POST)
#         form = MessageForm(request.POST)
#         if form.is_valid():
#             form.save()
#             status = 201
#         else:
#             print("TELL them that sent data is not valid")
#     messageForm = MessageForm()
#     return render(request, "contact.html", context= {"messageForm": messageForm}, status=status)



class NewsFilters(FilterView):
    model = News
    context_object_name = "news"
    filterset_class = NewsFilter

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        most_viewed_news = News.objects.order_by('-view_count')[:5]
        context['most_viewed_news'] = most_viewed_news
        return context
    
class Filter(LoginRequiredMixin, FilterView):
    template_name = "core/all_news.html"
    filterset_class = NewsFilter
    paginate_by = 3

    def get_queryset(self):
        queryset = super(Filter, self).get_queryset()
        queryset = queryset.filter(user=self.request.user)
        return queryset


class Home(NewsFilters):
    template_name = "index.html"
    paginate_by = 8

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super(Home, self).get_queryset()
        return queryset.order_by('-date')

    def post(self, request, *args, **kwargs):
        messageForm = MessageForm(request.POST)
        if messageForm.is_valid():
            messageForm.save()
            messages.success(request, "Your Message has been sent!")
        return redirect("{% url 'home'%}")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = NewsFilter(
            self.request.GET, queryset=self.get_queryset())
        return context


def category(request):
    news = News.objects.all()
    return render(request, "category.html", context={"news": news})


class Contact(Home):
    template_name = "contact.html"
