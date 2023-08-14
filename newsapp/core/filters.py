from django_filters import FilterSet, DateTimeFilter
from .models import News
from django import forms

class NewsFilter(FilterSet):
    date = DateTimeFilter("date", widget = forms.SelectDateWidget())
    class Meta:
        model = News
        fields = ("news_type", "title", "description", "date")