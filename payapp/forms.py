from django import forms
from django.forms import ModelChoiceField

from payapp.models import Transactions


class SendTransactionForm(forms.ModelForm):
    class Meta:
        model = Transactions
        fields = ('user_receiving', 'amount')

    def __init__(self, *args, user=None, **kwargs):
        super(SendTransactionForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['user_receiving'].queryset = self.fields['user_receiving'].queryset.exclude(pk=user.pk)

        self.fields['user_receiving'].label = "Send to"


class RequestTransactionForm(forms.ModelForm):
    class Meta:
        model = Transactions
        fields = ('user_sending', 'amount')

    def __init__(self, *args, user=None, **kwargs):
        super(RequestTransactionForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['user_sending'].queryset = self.fields['user_sending'].queryset.exclude(pk=user.pk)

        self.fields['user_sending'].label = "Request From"


class TransactionModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return f"ID: {obj.id}, Amount: {obj.amount}, To: {obj.user_receiving}"


class ProcessPendingForm(forms.Form):
    ACCEPT_OR_REJECT_CHOICES = (
        ('accept', 'Accept'),
        ('reject', 'Reject'),
    )

    action = forms.ChoiceField(choices=ACCEPT_OR_REJECT_CHOICES)
    transaction_id = TransactionModelChoiceField(queryset=Transactions.objects.all())

    class Meta:
        model = Transactions
        fields = ('transaction_id', 'action')

    def __init__(self, *args, user=None, **kwargs):
        super(ProcessPendingForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['transaction_id'].queryset = Transactions.objects.filter(user_sending=user, state='pending')

        self.fields['transaction_id'].label = "Transaction ID"
