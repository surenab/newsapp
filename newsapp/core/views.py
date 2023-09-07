from typing import Any, Dict
from django.shortcuts import render, redirect
from .models import *
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView, TemplateView
from .forms import NewsForm, MessageForm, NewsCommentForm, SetPasswordForm, UserProfileForm
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django_filters.views import FilterView
from .filters import NewsFilter
from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
# from django.contrib.auth.decorators import user_not_authenticated
from django.contrib.auth import get_user_model
from django.db.models.query_utils import Q
# from django.template.loader import render_to_string
# from django.core.mail import EmailMessage
# from django.utils.encoding import force_bytes
# from django.utils.http import urlsafe_base64_encode
# from django.contrib.sites.shortcuts import get_current_site
# from .token import account_activation_token




# Create your views here.
User = get_user_model()

# def profile(request):
#     news = News.objects.all()
#     return render(request=request, template_name="core/profile.html", context={"news": news})


class Profile(TemplateView):
    template_name = "core/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            profile = get_object_or_404(UserProfile, user=self.request.user)
            context['profile'] = profile

        return context

    def post(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            profile = self.request.user.profile
            form = UserProfileForm(request.POST, request.FILES, instance=profile)
            if form.is_valid():
                form.save()
                return redirect("{% url 'profile'%}")
            return render(request, 'core/profile.html', {'form': form})
        else:
            return redirect("{% url 'login'%}")


def update_profile(request):
    msg = None
    if request.method == "POST":
        form = UserProfile(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            msg = "Changes have been saved"
    
    form = UserProfile(instance=request.user)
    return render(request=request, template_name="core/edit-profile.html", context={"form": form, "msg": msg})


@login_required
def change_password(request):
    user = request.user
    if request.method == "POST":
        form = SetPasswordForm(user, request)
        if form.is_valid():
            form.save()
            messages.success(request, "Your password has been change!")
            return redirect("{% url 'profile'%}")
        else:

            for error in list(form.errors.value()):
                messages.error(request,error)

    form = SetPasswordForm(user)
    return render(request, 'core/password_change_form.html', {'form': form})


# @user_not_authenticated
# def parrword_reset_request(request):
#     if request.method == "POST":
#         form = PasswordResetForm(request.POST)
#         if form.is_valid():
#             user_email = form.cleaned_data["email"]
#             associated_user = get_user_model().objects.filter(Q[email == user_email]).first()
#             if associated_user:
#                 subject = "Password Reset Request"
#                 message = render_to_string("template_activate_account.html", 
#                 {
#                     'user': associated_user,
#                     'domain': get_current_site(request).domain,
#                     'uid': urlsafe_base64_encode(force_bytes(associated_user.pk)),
#                     'token': account_activation_token.make_token(associated_user),
#                     'protokol': 'https' if request.is_sequre() else 'http'
#                 }
#                 )
#                 email = EmailMessage(subject, message, to=[associated_user.email])
#                 if email.send():
#                     messages.success(request, "Please confirm your email address to complete the password reset")
#                 else:
#                     message.error(request, "Promlem with sending email")

#             return redirect("{% url 'home' %}")

#     form = PasswordResetForm()
#     return render(request=request, template_name = "core/password-reset.html", context={"form": form})

def password_reset_confirm(request, uidb64, token):
    return redirect("{% url 'login'%}")


def about(request):
    team = Team.objects.all()
    return render(request=request, template_name="about.html", context={"team": team}) 


class Base(LoginRequiredMixin):
    def get_queryset(self):
        queryset = super(Base, self).get_queryset()
        queryset = queryset.filter(user=self.request.user)
        return queryset


class NewsBase(Base):
    model = News
    context_object_name = "news"
    form_class = NewsForm
    success_url = reverse_lazy("all_news")
    success_text = ""
    
    def form_valid(self, form):
        messages.success(self.request, self.success_text)
        return super().form_valid(form)


class CreateNewsComment(CreateView):
    model = NewsComment
    form_class = NewsCommentForm
    success_text = "Created!"

    def get_success_url(self):
        return reverse_lazy("my_news_details", kwargs = {"pk": self.request.POST.get("news")})

    def form_valid(self, form):
        form.instance.owner = self.request.user
        news_id = self.request.POST.get("news")
        news = get_object_or_404(News, id = news_id)
        form.instance.news = news
        messages.success(self.request, "News Comment instance is created.")
        return super().form_valid(form)


class CreateNews(NewsBase, CreateView):
    template_name = "create_news.html"

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, "Your new post has been completed.")
        return super().form_valid(form)


class MyNews(NewsBase, FilterView):
    template_name = "core/news_list.html"
    filterset_class = NewsFilter
    paginate_by = 2


class MyNewsDetail(NewsBase, DetailView):
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        data = super().get_context_data(**kwargs)
        data["comment_form"] = NewsCommentForm
        data["comments"] = NewsComment.objects.filter(news=data["news"])
        return data

class NewsDetails(DetailView):
    model = News
    context_object_name = "news"
    template_name = "news-detail.html"

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['comment_form'] = NewsCommentForm
        data['comments'] = NewsComment.objects.filter(news=data["news"])
        return data

    def get(self, request: HttpRequest, *args, **kwargs):
        self.object = self.get_object()
        self.object.view_count += 1
        self.object.save()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)



class MyNewsUpdate(NewsBase, UpdateView):
    success_text = "News instance is updated!"


class MyNewsDelete(LoginRequiredMixin, DeleteView):
    model = News
    context_object_name = "news"
    success_url = reverse_lazy("my_news")

    def get_queryset(self):
        queryset = super(MyNewsDelete, self).get_queryset()
        queryset = queryset.filter(user=self.request.user)
        return queryset

    def form_valid(self, form):
        messages.info(self.request, "News instance is deleted!")
        return super().form_valid(form)



def search(request):
    news = News.objects.all()
    return render(request, "search-result.html", context={"news": news})

def single_post(request):
    news = News.objects.all()
    return render(request, "single-post.html", context={"news": news})


class NewsFilters(FilterView):
    model = News
    context_object_name = "news"
    filterset_class = NewsFilter

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        most_viewed_news = News.objects.order_by('-view_count')[:5]
        context['most_viewed_news'] = most_viewed_news
        return context
    
class Filter(LoginRequiredMixin, FilterView):
    template_name = "core/all_news.html"
    filterset_class = NewsFilter
    paginate_by = 3

    def get_queryset(self):
        queryset = super(Filter, self).get_queryset()
        queryset = queryset.filter(user=self.request.user)
        return queryset


class Home(NewsFilters):
    template_name = "index.html"
    paginate_by = 8

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super(Home, self).get_queryset()
        return queryset.order_by('-date')

    def post(self, request, *args, **kwargs):
        messageForm = MessageForm(request.POST)
        if messageForm.is_valid():
            messageForm.save()
            messages.success(request, "Your Message has been sent!")
        return redirect("{% url 'home'%}")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = NewsFilter(
            self.request.GET, queryset=self.get_queryset())
        return context


def category(request):
    news = News.objects.all()
    return render(request, "category.html", context={"news": news})


class Contact(Home):
    template_name = "contact.html"
