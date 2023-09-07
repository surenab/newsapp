from django.urls import path, include
from .views import Register
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('', include("django.contrib.auth.urls"), name = "login"),
    path('register/', Register.as_view(), name = "register"),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
