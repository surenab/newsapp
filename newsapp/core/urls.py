from django.urls import path
from .views import home, CreateNews, about, MyNews, MyNewsDetail, MyNewsUpdate, MyNewsDelete
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('', home, name = "home"),
    path('create-news', CreateNews.as_view(), name = "create_news"),
    path('about', about, name = "about"),
    # path('my-news', MyNews.as_view(), name = "my_news"),
    path("my-news/details/<int:pk>", MyNewsDetail.as_view(), name="my_news_details"),
    # path("my-news/update/<int:pk>", MyNewsUpdate.as_view(), name="my_news_update"),
    # path("my-news/delete/<int:pk>", MyNewsDelete.as_view(), name="my_news_delete"),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
