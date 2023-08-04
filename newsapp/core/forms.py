from django import forms
from .models import News

class NewsForm(forms.Form):
    NEWS_TYPES = (
        ("1", "Political"),
        ("2", "Business"),
        ("3", "International"),
        ("4","National"),
        ("5","Lifestyle"),
        ("6", "Sport"),
        ("7", "Entertainment"),
        ("8", "Crime")
    )

    news_type = forms.ChoiceField(choices=NEWS_TYPES)
    
    class Meta:
        model = News
        fields = ["title", "description", "news_type"]
