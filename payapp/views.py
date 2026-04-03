from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import render, redirect
from django.views.decorators.cache import never_cache
from . import models
from payapp.forms import TransactionForm, RequestTransactionFrom
from payapp.models import Transaction
from register.models import PayAppUser
from django.db.models import Q



def get_currency_symbol_helper(c):
    match c:
        case 'EUR':
            return '€'
        case 'USD':
            return '$'
        case 'GBP':
            return '$'
    return '?'


@never_cache    #dont cache so user cannot logout and return to logged in pag
def home(request):
    return render(request, 'index.html')

@login_required(login_url='login')
def new_transaction(request):
    form = TransactionForm()
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                payee_name = form.cleaned_data['payee']
                amount = form.cleaned_data['amount']
                payer = request.user
                payee = PayAppUser.objects.select_for_update().get(username=payee_name)
                if payer.balance < amount:
                    messages.error(request, "Your balance is too low!")
                    return redirect('new_transaction')

                payer.balance -= amount
                payer.save()

                payee.balance += amount
                payee.save()

                new_transaction_entry = form.save(commit=False)
                new_transaction_entry.payer = payer
                new_transaction_entry.payee = payee
                new_transaction_entry.status = 'COMPLETED'
                new_transaction_entry.save()
                return redirect('new_transaction')

    symbol = get_currency_symbol_helper(request.user.currency)
    return render(request, 'payapp/new-transaction.html', {'form': form, 'currency_symbol': symbol})

@login_required(login_url='login')
def request_transaction(request):
    form = RequestTransactionFrom()
    return render(request, 'payapp/request-transaction.html', {'form': form})

@login_required(login_url='login')
def user_transactions(request):
    username= request.user.username
    Transaction = models.Transaction.objects.filter(Q(payee__username=username)|Q(payer__username=username))
    transactions = Transaction.all().order_by('-time')
    user_currency = get_currency_symbol_helper(request.user.currency)
    return render(request, 'payapp/user-transactions.html',{'transactions':transactions, 'user_currency': user_currency})