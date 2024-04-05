from django.contrib.auth.models import User
from django.db import models


class Transactions(models.Model):
    STATE_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    )

    user_sending = models.ForeignKey(User, related_name='sent_transactions', on_delete=models.CASCADE)
    user_receiving = models.ForeignKey(User, related_name='received_transactions', on_delete=models.CASCADE)
    state = models.CharField(max_length=10, choices=STATE_CHOICES, default="pending", null=False)
    transaction_date = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=False)

    def __str__(self):
        details = ''
        details += f'Transaction Date Time   : {self.transaction_date}\n'
        details += f'User Sending         : {self.user_sending}\n'
        details += f'User Receiving       : {self.user_receiving}\n'
        details += f'State                : {self.state}\n'
        details += f'Amount                : {self.amount}\n'
        return details
