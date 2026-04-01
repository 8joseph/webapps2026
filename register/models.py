from django.db import models
from django.contrib.auth.models import AbstractUser

class PayAppUser(AbstractUser):
    CURRENCY_CHOICE = [
        ('EUR', 'Euro'),
        ('USD', 'US Dollar'),
        ('GBP', 'Great British Pound'),
    ]
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICE, default='EUR')
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)