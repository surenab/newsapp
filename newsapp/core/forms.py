from django import forms
from .models import News

class NewsForm(forms.ModelForm):
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

    news_type = forms.ChoiceField(choices=NEWS_TYPES)
    image = forms.ImageField(label="")
    class Meta:
        model = News

        fields = ["title", "description", "news_type", 'image']

