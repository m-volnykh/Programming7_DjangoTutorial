from django.shortcuts import render, redirect
from django.contrib.auth import login, mixins
from django.contrib.auth.views import LoginView
from django.views import generic
from django.contrib import messages

from .forms import RegisterForm, LoginForm

class ProfileView(mixins.LoginRequiredMixin, generic.TemplateView):
    template_name = "polls/profile.html"

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # автоматически логиним пользователя

            # сообщение об успешной регистрации
            messages.success(request, f"Аккаунт {user.username} успешно создан!")
            
            return redirect("login")
    else:
        form = RegisterForm()

    return render(request, "registration/register.html", {"form": form})

class CustomLoginView(LoginView):
    authentication_form = LoginForm
    template_name = "registration/login.html"