from django.urls import path
from .views import home, CreateNews, about
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('', home, name = "home"),
    path('create-news', CreateNews.as_view(), name = "create_news"),
    path('about', about, name = "about"),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
