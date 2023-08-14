import django_filters
from django_filters import DateFilter
from .models import News 
from django import forms


class NewsFilters(django_filters.FilterSet):
    date= DateFilter('date', widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    class Meta:
        model = News
        fields = ("title", "news_type", "date", "description")
        
