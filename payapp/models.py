from django.db import models
from django.utils import timezone

from register import models as reg_models

class Transaction(models.Model):
    STATUS_OPTIONS = (
        ('PENDING', 'PENDING'),
        ('COMPLETED', 'COMPLETED'),
        ('REJECTED', 'REJECTED')
    )
    CURRENCY_CHOICE = [
        ('EUR', 'Euro'),
        ('USD', 'US Dollar'),
        ('GBP', 'Great British Pound'),
    ]
    payer = models.ForeignKey(reg_models.PayAppUser,related_name='payer', on_delete=models.CASCADE)
    payee = models.ForeignKey(reg_models.PayAppUser,related_name='payee' ,on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=100, decimal_places=2)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICE, default='EUR')
    status = models.CharField(max_length=10, choices=STATUS_OPTIONS, default='REJECTED')
    time = models.DateTimeField(default=timezone.now)