from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse

from users.forms import RegistrationForm, LoginForm, UserUpdateForm


def registration_view(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("products:list")

    else:
        form = RegistrationForm()

    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.method == "POST":
        form = LoginForm(data=request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)

            if user:
                login(request, user)
                return redirect("products:list")

    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})


@login_required
def profile_view(request):
    if request.method == "POST":
        form = UserUpdateForm(request.POST, request.FILES, instance=request.user)

        if form.is_valid():
            form.save()
            return redirect("users:profile")

    else:
        form = UserUpdateForm(instance=request.user)

    return render(request, 'profile.html', {'user': request.user, 'form': form})
