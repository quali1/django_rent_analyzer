from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render, redirect

from analyzer.models import OtodomData
from analyzer.models import Offer
from .models import UserProfile
from django.http import HttpResponseRedirect


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


# def user_profile(request, pk):
#     sort_value = 'newest'
#     method_value = None
#     site_value = None
#     sort_mapping = {
#         "newest": ["-created", "Newest First"],
#         "oldest": ["created", "Oldest First"],
#     }
#
#     user = User.objects.get(id=pk)
#     requests = OtodomData.objects.filter(requester=user).order_by('-created').all()
#
#     if request.method == "POST":
#         print(request.POST)
#         sort_value = request.POST.get('sort_value', 'newest')
#         method_value = request.POST.get('method_value', '')
#         site_value = request.POST.get('site_value', '')
#
#         # requests = OtodomData.objects.filter(method=method_value,
#         #                                      requester=user,
#         #                                      site=site_value).order_by(sort_mapping[sort_value][0]).all()
#
#         requests = OtodomData.objects.filter(
#             Q(requester=user)
#             & Q(site=site_value if site_value else '')
#             & Q(method=method_value)
#         ).order_by(sort_mapping[sort_value][0]).all()
#
#         print(requests)
#
#     context = {
#         "user": user,
#         "requests": requests,
#         "sort_mapping": sort_mapping,
#         "sort_value": sort_value,
#         "method_value": method_value,
#         "site_value": site_value,
#     }
#
#     return render(request, "users/user-profile.html", context)

def user_profile(request, pk):
    # Mapping for sorting options
    sort_mapping = {
        "newest": ["-created", "Newest First"],
        "oldest": ["created", "Oldest First"],
    }

    # Available methods and sites
    methods = ["ai", "manual"]
    sites = ["otodom", "site2"]

    # Retrieve user and user profile
    user = User.objects.get(id=pk)
    user_profile = UserProfile.objects.get(user=user)

    # Retrieve saved offers for the user
    saved_offers = user_profile.saved_offers.all()

    # Default values
    sort_value = 'newest'
    method_value = request.POST.get('method_value', '')
    site_value = request.POST.get('site_value', '')

    # Retrieve requests associated with the user
    requests = OtodomData.objects.filter(requester=user)

    # Filter requests based on method and site values if provided
    if method_value:
        requests = requests.filter(method=method_value)
    if site_value:
        requests = requests.filter(site=site_value)

    # Handle sorting based on POST data
    if request.method == "POST":
        sort_value = request.POST.get('sort_value', 'newest')

    # Set sorting key based on sort_value
    sort_key = '-created' if sort_value == 'newest' else 'created'
    requests = requests.order_by(sort_key)

    # Context data for rendering
    context = {
        "user": user,
        "requests": requests,
        "sort_value": sort_value,
        "method_value": method_value,
        "site_value": site_value,
        "sort_mapping": sort_mapping,
        "methods": methods,
        "sites": sites,
        "saved_offers": saved_offers,
    }

    return render(request, "users/user-profile.html", context)


def save_offer(request, article_id):
    user = request.user.userprofile
    offer = Offer.objects.get(article_id=article_id)
    user.saved_offers.add(offer)

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def remove_offer(request, article_id):
    user = request.user.userprofile
    offer = Offer.objects.get(article_id=article_id)
    user.saved_offers.remove(offer)

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
