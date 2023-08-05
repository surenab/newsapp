from django.urls import path
from .views import home, CreateNews
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('', home, name = "home"),
    path('create-news', CreateNews.as_view(), name = "create_news"),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
