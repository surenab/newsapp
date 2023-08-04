from django.urls import path
from .views import home, CreateNews

urlpatterns = [
    path('', home, name = "home"),
    path('create-news', CreateNews.as_view(), name = "create_news"),
]
