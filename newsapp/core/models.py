from django.db import models

# Create your models here.
class News(models.Model):

    NEWS_TYPES = (
        ("1", "Urgent"),
        ("2", "Regular"),
        ("3", "Low")
    )

    title = models.CharField(max_length=100)
    content = models.TextField()
    author = models.CharField(max_length=100)
    publication_date = models.DateTimeField(auto_now_add=True)
    newsapp_type = models.CharField(choices=NEWS_TYPES, default="2", max_length=1)

    def __str__(self):
        return f"{self.title}"
