from django import forms
from .models import Transaction

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['payee', 'amount']

class RequestTransactionFrom(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['payer', 'amount']