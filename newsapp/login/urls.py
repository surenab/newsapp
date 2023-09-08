from django.urls import path, include
from .views import Register
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path('', include("django.contrib.auth.urls")),
    path('register/', Register.as_view(), name = "register"),
    path('registration-success/', views.registration_success, name='registration-success'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
