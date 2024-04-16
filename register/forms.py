from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from register.models import Accounts


class RegisterForm(UserCreationForm):
    CURRENCY_CHOICES = (
        ('usd', 'USD'),
        ('gbp', 'GBP'),
        ('eur', 'EUR'),
    )

    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    currency = forms.ChoiceField(choices=CURRENCY_CHOICES)

    class Meta:
        model = User
        fields = (
            "first_name", "last_name", "username", "email", "password1", "password2", "currency",
        )

    def save(self, *args, **kwargs):
        instance = super(RegisterForm, self).save(*args, **kwargs)

        Accounts.objects.create(username=instance, amount=1000, currency=self.cleaned_data['currency'])
        return instance


class PromoteAdminForm(forms.Form):
    username = forms.ModelChoiceField(
        queryset=User.objects.filter(is_superuser=False),
        label="User to Promote"
    )

    class Meta:
        model = User
        fields = ("username",)

    def promote_user(self):
        user = self.cleaned_data['username']
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user
