from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.views.decorators.cache import never_cache
from . import models
from payapp.forms import TransactionForm, RequestTransactionFrom
from payapp.models import Transaction
from register.models import PayAppUser
from django.db.models import Q
import requests



def get_currency_symbol_helper(c):
    match c:
        case 'EUR':
            return '€'
        case 'USD':
            return '$'
        case 'GBP':
            return '£'
    return '?'


@never_cache    #dont cache so user cannot logout and return to logged in page
def home(request):
    currency = get_currency_symbol_helper(request.user.currency)
    username = request.user.username
    transactions = models.Transaction.objects.filter((Q(payee__username=username)|Q(payer__username=username)) & (Q(status="COMPLETED"))).all().order_by('-time')[:5]
    pending_transactions = len(models.Transaction.objects.filter((Q(payer__username=username)) & Q(status="PENDING")).all())

    return render(request, 'index.html',{'currency_symbol': currency, 'recent_transactions': transactions, 'pending_transactions': pending_transactions})

@login_required(login_url='login')
def new_transaction(request):
    form = TransactionForm()
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                payee_user = form.cleaned_data['payee']
                payer_amount = form.cleaned_data['payer_amount']
                payer = request.user
                payee = PayAppUser.objects.select_for_update().get(id=payee_user.id)

                payee_amount = call_conversion_api(payer.currency, payee.currency, payer_amount)
                if payee_amount is None:
                    messages.error(request, "Currency conversion API failed.")
                    return redirect('new_transaction')


                if payer.balance < payer_amount:
                    messages.error(request, "Your balance is too low!")
                    return redirect('new_transaction')
                if payer == payee:
                    messages.error(request, "You cannot send money to yourself!")
                    return redirect('new_transaction')

                payer.balance -= payer_amount
                payer.save()

                payee.balance += payee_amount
                payee.save()

                new_transaction_entry = form.save(commit=False)
                new_transaction_entry.payer = payer
                new_transaction_entry.payer_amount = payer_amount
                new_transaction_entry.payer_currency = request.user.currency
                new_transaction_entry.payee = payee
                new_transaction_entry.payee_amount = payee_amount
                new_transaction_entry.payee_currency = payee.currency
                new_transaction_entry.status = 'COMPLETED'
                new_transaction_entry.save()
                messages.success(request, "Transaction sent!")
                return redirect('new_transaction')

    symbol = get_currency_symbol_helper(request.user.currency)
    return render(request, 'payapp/new-transaction.html', {'form': form, 'currency_symbol': symbol})

@login_required(login_url='login')
def request_transaction(request):
    form = RequestTransactionFrom()
    if request.method == "POST":
        form = RequestTransactionFrom(request.POST)
        if form.is_valid():
            payer = form.cleaned_data['payer']
            payee_amount = form.cleaned_data['payee_amount']

            payer_amount = call_conversion_api(request.user.currency, payer.currency, payee_amount)
            if payee_amount <= 0:
                messages.error(request, "Amount requested must be greater than 0!")
                return redirect('request_transaction')
            if request.user == payer:
                messages.error(request, "You cannot request money from yourself!")
                return redirect('request_transaction')
            new_transaction_entry = form.save(commit=False)
            new_transaction_entry.payer = payer
            new_transaction_entry.payer_amount = payer_amount
            new_transaction_entry.payer_currency = payer.currency
            new_transaction_entry.payee = request.user
            new_transaction_entry.payee_amount = payee_amount
            new_transaction_entry.payee_currency = request.user.currency
            new_transaction_entry.status = 'PENDING'
            new_transaction_entry.save()
            messages.success(request, f"Request was sent to {payer.username}")
            return redirect('request_transaction')

    return render(request, 'payapp/request-transaction.html', {'form': form})

@login_required(login_url='login')
def user_transactions(request):
    username= request.user.username

    transactions = models.Transaction.objects.filter(Q(payee__username=username)|Q(payer__username=username)).all().order_by('-time')
    pending_transactions = models.Transaction.objects.filter((Q(payer__username=username)) & Q(status="PENDING")).all().order_by('-time')
    user_currency = get_currency_symbol_helper(request.user.currency)
    return render(request, 'payapp/user-transactions.html',{'transactions':transactions,'pending_transactions':pending_transactions, 'user_currency': user_currency})

@login_required(login_url='login')
def accept_transaction_request(request, transaction_id):
    if request.method == "POST":
        t = get_object_or_404(Transaction, id=transaction_id)
        if t.payer != request.user:
            messages.error(request, "You are unable to accept this transaction!")
            return redirect('user-transactions')

        if t.status != 'PENDING':
            messages.error(request, "This transaction has already been processed!")
            return redirect('user-transactions')
        with transaction.atomic():
            payer = PayAppUser.objects.select_for_update().get(id=t.payer.id)
            payee = PayAppUser.objects.select_for_update().get(id=t.payee.id)
            if payer.balance < t.payer_amount:
                messages.error(request, "Your balance is too low to accept this transaction!")
                return redirect('user-transactions')
            payer.balance -= t.payer_amount
            payee.balance += t.payee_amount
            payer.save()
            payee.save()
            t.status = 'COMPLETED'
            t.time = timezone.now()
            t.save()
            messages.success(request, "Transaction successfully transferred")

    return redirect('user-transactions')

@login_required(login_url='login')
def decline_transaction_request(request, transaction_id):
    if request.method == "POST":
        t = get_object_or_404(Transaction, id=transaction_id)
        if t.payer != request.user:
            messages.error(request, "You are unable to decline this transaction!")
            return redirect('user-transactions')
        if t.status != 'PENDING':
            messages.error(request, "This transaction has already been processed!")
            return redirect('user-transactions')
        t.status = 'REJECTED'
        t.time = timezone.now()
        t.save()
        messages.success(request, "Transaction has been declined")

    return redirect('user-transactions')

#function for calling the REST api
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
