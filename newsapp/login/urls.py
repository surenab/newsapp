from django.urls import path, include
from .views import Register, terms_conditions, ProfileTemplate, update_profile, change_password
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('', include("django.contrib.auth.urls"), name = "login"),
    path('register/', Register.as_view(), name = "register"),
    path("terms-conditions/", terms_conditions, name="terms_conditions"),
    path('profile/', ProfileTemplate.as_view(), name = "profile"),
    path('update-profile/', update_profile, name = "update_profile"),
    path('change-password/', change_password, name = "change_password"),
    # path("parrword-reset", parrword_reset_request, name = "parrword_reset"),
    # path("eset/<uidb64>/<token>/", password_reset_confirm, name = "reset_confirm"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
