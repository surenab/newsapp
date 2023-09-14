from django.shortcuts import render
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import RegisterForm, ProfileForm, SetPasswordForm, PasswordResetForm
from django.contrib.auth import login
from django.shortcuts import redirect
from django.contrib import messages
from django.shortcuts import get_object_or_404, get_list_or_404
from django.views.generic import CreateView, TemplateView
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .models import Profile
# from django.contrib.auth.decorators import user_not_authenticated
# from django.template.loader import render_to_string
# from django.core.mail import EmailMessage
# from django.utils.encoding import force_bytes
# from django.utils.http import urlsafe_base64_encode
# from django.contrib.sites.shortcuts import get_current_site
# from django.contrib.auth.tokens import account_activation_token
# from django.contrib.auth import get_user_model


# Create your views here.

class Register(CreateView):
    form_class = RegisterForm
    success_url = reverse_lazy("login")
    template_name = "registration/register.html"

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        messages.success(self.request, "Registration was successful. You are now logged in. You can edit your profile information by clicking the 'Edit Profile' button.")
        return redirect("profile")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


def terms_conditions(request):
    return render(request, "registration/terms-conditions.html")


class ProfileTemplate(TemplateView):
    template_name = "core/profile.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
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
    msg = None
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            msg = "Changes have been saved"
    
    form = ProfileForm(instance=request.user.profile)
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


# def password_reset_request(request):
#     if request.method == "POST":
#         form = PasswordResetForm(request.POST)
#         if form.is_valid():
#             user_email = form.cleaned_data["email"]
#             associated_user = get_user_model().objects.filter(email=user_email).first()
#             if associated_user:
#                 subject = "Password Reset Request"
#                 message = render_to_string("template_activate_account.html", 
#                 {
#                     'user': associated_user,
#                     'domain': get_current_site(request).domain,
#                     'uid': urlsafe_base64_encode(force_bytes(associated_user.pk)),
#                     'token': account_activation_token.make_token(associated_user),
#                     'protocol': 'https' if request.is_secure() else 'http'
#                 }
#                 )
#                 email = EmailMessage(subject, message, to=[associated_user.email])
#                 if email.send():
#                     messages.success(request, "Please confirm your email address to complete the password reset")
#                 else:
#                     messages.error(request, "Problem with sending email")

#             return redirect('home')

#     form = PasswordResetForm()
#     return render(request=request, template_name="core/password-reset.html", context={"form": form})


# def password_reset_confirm(request, uidb64, token):
#     return redirect("{% url 'login'%}")
