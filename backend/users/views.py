from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render, redirect

from analyzer.models import OtodomData


# Create your views here.

def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username").lower()
        password = request.POST.get("password").lower()

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Invalid username or password!")

    return render(request, "users/login.html")


def user_register(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.success(request, "You have singed up successfully.")
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "An error occurred during Registration")

    context = {"form": form}

    return render(request, "users/register.html", context)


@login_required(login_url="home")
def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect("home")


def user_profile(request, pk):
    user = User.objects.get(id=pk)
    requests = OtodomData.objects.filter(requester=user).all()

    context = {
        "user": user,
        "requests": requests,
    }

    return render(request, "users/user-profile.html", context)
