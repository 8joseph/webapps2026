from django import forms
from django.contrib.auth.models import User

from register.models import PayAppUser
from .models import Transaction

class TransactionForm(forms.ModelForm):
    payee = forms.CharField(label='Payee', max_length=100)
    class Meta:
        model = Transaction
        fields = ['payee', 'amount']

    def clean_payee(self):
        payee_name = self.cleaned_data.get('payee')
        try:
            user = PayAppUser.objects.get(username=payee_name)
            return user
        except PayAppUser.DoesNotExist:
            raise forms.ValidationError("payee does not exist")

class RequestTransactionFrom(forms.ModelForm):
    payer = forms.CharField(label='Payer', max_length=100)
    class Meta:
        model = Transaction
        fields = ['payer', 'amount']

    def clean_payer(self):
        payer_name = self.cleaned_data.get('payer')
        try:
            user = PayAppUser.objects.get(username=payer_name)
            return user
        except PayAppUser.DoesNotExist:
            raise forms.ValidationError("payer does not exist")