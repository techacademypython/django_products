from django.shortcuts import render, redirect
from .forms import RegistrationForm, LoginForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


# Create your views here.

def register_view(request):
    if not request.user.is_authenticated:
        context = {}
        context["form"] = RegistrationForm()
        if request.method == "POST":
            form = RegistrationForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                user.set_password(request.POST.get("password"))
                user.save()
                messages.success(
                    request, "Ugurla qeydiyyatdan kecdiniz"
                )
                return redirect("login_view")
            else:
                messages.error(
                    request, "Formda problem var`"
                )
                context["form"] = form
        return render(request, "register.html", context)
    else:
        return redirect("dashboard")


def login_view(request):
    if not request.user.is_authenticated:
        context = {}
        context["form"] = LoginForm()
        if request.method == "POST":
            form = LoginForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data.get("username")
                password = form.cleaned_data.get("password")
                user = authenticate(username=username, password=password)
                if user:
                    if user.is_active:
                        messages.success(
                            request, "Daxil oldunuz"
                        )
                        login(request, user)
                        return redirect("dashboard")
                    else:
                        messages.error(
                            request, "Istifadeci aktiv deyil"
                        )
                        context["form"] = form
                else:
                    messages.error(
                        request, "Bele bir user movcud deyil"
                    )
                    context["form"] = form
            else:
                messages.error(
                    request, "Bele bir user movcud deyil"
                )
                context["form"] = form
        return render(request, "login.html", context)
    else:
        return redirect("dashboard")


def logout_view(request):
    logout(request)
    return redirect('login_view')
