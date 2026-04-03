from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.cache import never_cache

from payapp.forms import TransactionForm, RequestTransactionFrom
from payapp.models import Transaction


@never_cache    #dont cache so user cannot logout and return to logged in pag
def home(request):
    return render(request, 'index.html')

@login_required(login_url='login')
def new_transaction(request):
    form = TransactionForm()
    return render(request, 'payapp/new-transaction.html', {'form': form})

@login_required(login_url='login')
def request_transaction(request):
    form = RequestTransactionFrom()
    return render(request, 'payapp/request-transaction.html', {'form': form})

@login_required(login_url='login')
def user_transactions(request):
    return render(request, 'payapp/user-transactions.html')