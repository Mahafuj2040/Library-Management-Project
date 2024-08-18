from django import forms
from .models import Transactions

class DepositForm(forms.ModelForm):
    class Meta:
        model = Transactions
        fields = ['amount']
