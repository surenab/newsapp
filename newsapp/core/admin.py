from django.contrib import admin
from .models import News, Team, Message, NewsComment

# Register your models here.
admin.site.register(News)
admin.site.register(Team)
admin.site.register(Message)
admin.site.register(NewsComment)
