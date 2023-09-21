from django.shortcuts import render
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import RegisterForm, ProfileForm, SetPasswordForm
from django.contrib.auth import login
from django.shortcuts import redirect
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.views.generic import CreateView, TemplateView
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .models import Profile
from core.models import Info


# Create your views here.

class Register(CreateView):
    form_class = RegisterForm
    success_url = reverse_lazy("profile")
    template_name = "registration/register.html"

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        messages.success(self.request, "Registration was successful. You are now logged in. You can edit your profile information by clicking the 'Edit Profile' button.")
        return redirect("profile")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        info_instance = Info.objects.all()
        context['info'] = info_instance
        return context


def terms_conditions(request):
    return render(request, "registration/terms-conditions.html")


class ProfileTemplate(TemplateView):
    template_name = "core/profile.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        info_instance = Info.objects.all()
        context['info'] = info_instance

        if self.request.user.is_authenticated:
            profile = get_object_or_404(Profile, user__username=self.request.user)
            context['profile'] = profile

        return context

    def post(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            profile = self.request.user.profile
            form = ProfileForm(request.POST, request.FILES, instance=profile)
            if form.is_valid():
                form.save()
                return redirect('profile')
            return render(request, 'core/profile.html', {'form': form})
        else:
            return redirect('{% url "login" %}')


def update_profile(request):
    info = Info.objects.all()
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Changes have been saved!")
            return redirect("profile")
    else:
        form = ProfileForm(instance=request.user.profile)
    return render(request=request, template_name="core/edit-profile.html", context={"form": form, "info": info,})



@login_required
def change_password(request):
    info = Info.objects.all()
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
    return render(request, 'core/password_change_form.html', {'form': form, "info": info,})
