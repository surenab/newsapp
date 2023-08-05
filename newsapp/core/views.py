from django.shortcuts import render
from .models import News
from django.views.generic import CreateView
from .forms import NewsForm
from django.urls import reverse_lazy

# Create your views here.

def home(request):
    news = News.objects.all()
    return render(request=request, template_name="index.html", context={"news": news})


class CreateNews(CreateView):
    form_class = NewsForm
    success_url = reverse_lazy("home")
    template_name = "create_news.html"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)