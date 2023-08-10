from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
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

    def __str__(self):
        return f"{self.title}"


class Team(models.Model):
    team_member=models.CharField(max_length=30)
    position=models.CharField(max_length=30)
    description=models.TextField(max_length=300)
    image = models.ImageField(upload_to='images/', null=True, blank=True)

    def __str__(self):
        return f"{self.team_member}" 

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_id': self.pk})
