
from django_filters import FilterSet, DateFilter, NumberFilter
from django import forms
from .models import News


class NewsFilter(FilterSet):
    date = DateFilter(field_name="date", widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))


    class Meta:
        model = News
        fields = ('date', 'news_type', 'user')
