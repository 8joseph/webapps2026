import requests
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
            user = form.save(commit=False)
            #amount of money for new user is £200
            user.balance = call_conversion_api('GBP', user.currency, 200)
            user.save()
            return redirect('login')
    else:
        form = RegisterPayAppUserForm()
    return render(request, 'register/register.html', {'form': form})


def logout_user(request):
    logout(request)
    return redirect('login')



def call_conversion_api(cur1 ,cur2, amount):
    url = f'https://127.0.0.1:8000/webapps2026/conversion/{cur1}/{cur2}/{amount}/'
    print("api function called")
    try:
        response = requests.get(url, verify=False)#verify needs to be false otherwise https will be rejected
        print("response")
        if response.status_code == 200:
            print("status code 200")
            data = response.json()
            new_amount = data['amount']
            return new_amount
        else:
            return None
    except:
        return None

