from django.contrib.auth.models import User
from django.db import models


class Accounts(models.Model):
    CURRENCY_CHOICES = (
        ('usd', 'USD'),
        ('gbp', 'GBP'),
        ('eur', 'EUR'),
    )
    username = models.ForeignKey(User, on_delete=models.CASCADE)

    amount = models.DecimalField(max_digits=10, decimal_places=2, default=1000)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, null=False)

    def __str__(self):
        details = ''
        details += f'Username   : {self.username}\n'
        details += f'Amount     : {self.amount}\n'
        details += f'Currency   : {self.currency}\n'
        return details
