from django.db import models
from register import models as reg_models

class Transaction(models.Model):
    STATUS_OPTIONS = (
        ('PENDING', 'PENDING'),
        ('COMPLETED', 'COMPLETED'),
        ('REJECTED', 'REJECTED')
    )
    payer = models.ForeignKey(reg_models.PayAppUser,related_name='payer', on_delete=models.CASCADE)
    payee = models.ForeignKey(reg_models.PayAppUser,related_name='payee' ,on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=100, decimal_places=2)
    time = models.DateTimeField(auto_now_add=True)
