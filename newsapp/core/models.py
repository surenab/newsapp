from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from PIL import Image
from django.contrib.auth.models import User


# Create your models here.
User = get_user_model()

class News(models.Model):

    NEWS_TYPES = (
        ("1", "Political"),
        ("2", "Business"),
        ("3", "International"),
        ("4","National"),
        ("5","Lifestyle"),
        ("6", "Sport"),
        ("7", "Cultural"),
        ("8", "Crime")
    )

    title = models.CharField(max_length=150)
    description = models.TextField()
    date = models.DateTimeField(auto_now=True)
    news_type = models.CharField(choices=NEWS_TYPES, default="4", max_length=1)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/', default=None, null=True, blank=True)
    view_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.title}, {self.news_type}, {self.user},{self.date}"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)

        if img.height > 400 or img.width > 700:
            output_size = (400, 700)
            img.thumbnail(output_size)
            img.save(self.image.path)


class Team(models.Model):
    team_member=models.CharField(max_length=30)
    position=models.CharField(max_length=30)
    description=models.TextField(max_length=300)
    image = models.ImageField(upload_to='images/', null=True, blank=True)

    def __str__(self):
        return f"{self.team_member}" 

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_id': self.pk})


class Message(models.Model):
    full_name = models.CharField(max_length=50)
    email = models.EmailField()
    subject = models.CharField(max_length=100)
    message = models.TextField(max_length=1000)
    date = models.DateTimeField(auto_now_add=True, blank = True, null = True)

    def __str__(self) -> str:
        return f"{self.full_name}, {self.date}"


class NewsComment(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    news = models.ForeignKey(News, on_delete=models.CASCADE)
    text = models.TextField(max_length=500)

    def __str__(self) -> str:
        return f"{self.owner.username} is commented {self.text}"
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='asets/img/albert.jpg', upload_to='images')
    tel = models.CharField(max_length=15, blank=True, null=True)
    address = models.CharField(max_length=200, blank=True, null=True)
    birthday = models.DateField()

    def __str__(self):
        return f'{self.user.username} Profile'
