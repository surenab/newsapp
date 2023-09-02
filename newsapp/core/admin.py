from django.contrib import admin
from .models import News, Team, Message, NewsComment
from django.core.mail import send_mail, BadHeaderError


class MessageAdmin(admin.ModelAdmin):
    list_display = ["full_name", "email", "subject"]
    def save_model(self, request, obj, form, change):
        recipients = [
            obj.email, 
        ]
        super().save_model(request, obj, form, change)

# Register your models here.
admin.site.register(News)
admin.site.register(Team)
admin.site.register(NewsComment)
admin.site.register(Message, MessageAdmin)
