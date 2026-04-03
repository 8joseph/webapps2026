from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from register.forms import RegisterPayAppUserForm


def login_user(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request,user)
            return redirect('home')
        # else:
        #     messages.error(request, 'Username/Password Incorrect')
    else:
            form = AuthenticationForm()
    return render(request, 'register/login.html', {'form': form})


def register_user(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = RegisterPayAppUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegisterPayAppUserForm()
    return render(request, 'register/register.html', {'form': form})


def logout_user(request):
    logout(request)
    return redirect('login')
