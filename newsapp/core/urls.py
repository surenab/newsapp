from django.urls import path
from .views import Home, CreateNews, about,get_streaming_video, MyNews, MyNewsDetail, MyNewsUpdate,MyNewsDelete,subscribe_success, search_result, search_suggestions, single_post, Contact, Filter, category, CreateNewsComment, NewsDetails, subscribe
from django.conf.urls.static import static
from . import views

from django.conf import settings


urlpatterns = [
    path('', Home.as_view(), name = "home"),
    path('my-news/create-news', CreateNews.as_view(), name = "create_news"),
    path('about', about, name = "about"),
    path('my-news', MyNews.as_view(), name = "my_news"),
    path("my-news/details/<int:pk>", MyNewsDetail.as_view(), name="my_news_details"),
    path("my-news/update/<int:pk>", MyNewsUpdate.as_view(), name="my_news_update"),
    path("my-news/delete/<int:pk>", MyNewsDelete.as_view(), name="my_news_delete"),
    path("search/", search_result, name="search_result"),
    path('search-suggestions/', search_suggestions, name='search_suggestions'),
    path("single-post/", single_post, name="single_post"),
    path('contact/', Contact.as_view(), name = "contact"),
    path('filter/', Filter.as_view(), name = "filter"),
    path('category/', category, name = "category"),
    path('create-comment', CreateNewsComment.as_view(), name = "create_comment"),
    path("details/<int:pk>", NewsDetails.as_view(), name="news_details"),
    path('subscribe/', subscribe, name='subscribe'),
    path('subscribe/success/', subscribe_success, name='subscribe_success'),
    # path('video_hosting.urls', video_hosting.urls, name='video_hosting'),
    # path('stream/<int:pk>/', get_streaming_video, name='stream'),
    # path('<int:pk>/', views.get_video, name='video'),
    # path('', views.get_list_video, name='home'),
 

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
