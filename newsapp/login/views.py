from django.shortcuts import render, redirect
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import RegisterForm
from django.contrib import messages


# Create your views here.

class Register(CreateView):
    form_class = RegisterForm
    success_url = reverse_lazy("registration-success")
    template_name = "registration/register.html"

def register(request):
    if request.method == 'POST':
        
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            
            messages.success(request, 'Registration successful!')
            return redirect('registration-success')
    else:
        form = RegisterForm()

    return render(request, 'registration/register.html', {'form': form})

def registration_success(request):
    return render(request, 'registration/registration_success.html')