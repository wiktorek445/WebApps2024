from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_protect

from payapp.models import Transactions
from register.forms import RegisterForm, PromoteAdminForm
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse
from django.shortcuts import render, redirect
from register.forms import RegisterForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages

from register.models import Accounts


@csrf_protect
def register_user(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Registration successful.")
            return redirect("login")
        else:
            messages.error(request, "Unsuccessful registration. Invalid information.")
            return render(request, "register/register.html", {"register_user": form})
    else:
        if request.user.is_authenticated:
            return redirect("home")
        else:
            form = RegisterForm()
            return render(request, "register/register.html", {"register_user": form})


def admin_view(request):
    if not request.user.is_superuser:
        messages.error(request, 'You are not authorized to access this page.')
        return redirect("home")
    if request.method == "POST":
        # If the form is submitted for promoting a user
        form = PromoteAdminForm(request.POST)
        if form.is_valid():
            user_to_promote = form.promote_user()
            messages.success(request, f"Successfully promoted {user_to_promote.username} to admin.")
            return redirect("admin_view")  # Redirect to the admin page after successful promotion
        else:
            messages.error(request, 'Promotion process failed')
            # If form validation fails, render the admin page with error messages
            transaction_list = Transactions.objects.all().order_by('-transaction_date')
            user_list = Accounts.objects.all().select_related('username')
            return render(request, 'register/admin.html', {
                'transaction_list': transaction_list,
                'user_list': user_list, 'promote': form
            })
    else:
        # If it's a GET request, simply render the admin page with the form
        form = PromoteAdminForm()
        transaction_list = Transactions.objects.all().order_by('-transaction_date')
        user_list = Accounts.objects.all().select_related('username')
        return render(request, 'register/admin.html', {
            'transaction_list': transaction_list,
            'user_list': user_list, 'promote': form
        })


@csrf_protect
def login_user(request):
    if request.method == "POST":
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("home")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        if request.user.is_authenticated:
            return redirect("admin")
        else:
            form = AuthenticationForm()
    return render(request, "register/login.html", {"login_user": form})


def logout_user(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("home")


def home(request):
    if request.user.is_authenticated:
        transaction_list = Transactions.objects.select_related().filter(
            Q(user_sending_id=request.user) | Q(user_receiving_id=request.user)
        ).order_by('-transaction_date')
    else:
        transaction_list = []

    return render(request, "register/home.html", {"transaction_list": transaction_list})


def is_superuser(user):
    return user.is_authenticated and user.is_superuser
