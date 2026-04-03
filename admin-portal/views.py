from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from payapp import models as payapp_models

from payapp.models import Transaction
from register import forms

def check_admin(u):
    if u.is_superuser:
        return True
    return False

@user_passes_test(check_admin)
def admin_accounts(request): #maybe change the name of this - slightly misleading
    User = get_user_model()
    users = User.objects.all()
    return render(request, 'admin-portal/admin-accounts.html',{'users':users})

@user_passes_test(check_admin)
def register_new_admin(request):
    if request.method == 'POST':
        form = forms.RegisterPayAppUserForm(request.POST)
        if form.is_valid():
            u = form.save(commit=False)
            u.is_superuser = True
            u.save()
            return redirect('home')
    else:
        form = forms.RegisterPayAppUserForm()
    return render(request, 'admin-portal/register-new-admin.html', {'form': form})

@user_passes_test(check_admin)
def admin_transactions(request):
    Transaction = payapp_models.Transaction.objects.all()
    transactions = Transaction.all().order_by('-time')
    return render(request, 'admin-portal/admin-all-transactions.html', {'transactions':transactions})


