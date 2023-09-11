from django.db import models
from PIL import Image
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model


# Create your models here.
User = get_user_model()

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tel = models.CharField(max_length=13, default=None, blank=True, null=True)
    address = models.CharField(max_length=100, default=None, blank=True, null=True)
    image = models.ImageField(upload_to="images", default=None, null=True, blank=True)


    def __str__(self):
        return f"User is {self.user.username}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    User.profile = property(lambda u: Profile.objects.get_or_create(user=u)[0])
