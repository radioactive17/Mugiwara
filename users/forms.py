from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from .models import *


class UserUpdateForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', ]
    
    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)

        if self.instance.id:
            self.fields['username'].disabled = True

class BankingUserUpdateForm(ModelForm):
    class Meta:
        model = BankingUser
        fields = "__all__"
        exclude = ['user']
        
    def __init__(self, *args, **kwargs):
        super(BankingUserUpdateForm, self).__init__(*args, **kwargs)

        if self.instance.id:
            self.fields['user_type'].disabled = True
    
    
    
from django import forms
from .models import Transactions

class Transactions_form(forms.ModelForm):
    class Meta:
        model = Transactions
        fields = ['from_account', 'to_account', 'amount']

    def __init__(self, *args, **kwargs):
        super(Transactions_form, self).__init__(*args, **kwargs)

        # Remove the drop-down in the 'from_account' field
        self.fields['from_account'].widget = forms.HiddenInput()

        # Exclude the current user from the 'to_account' choices
        current_user_account = kwargs.get('initial', {}).get('from_account')
        if current_user_account:
            self.fields['to_account'].queryset = self.fields['to_account'].queryset.exclude(pk=current_user_account.pk)


class DebitForm(forms.Form):
    amount = forms.IntegerField(
        label='Amount',
        min_value=1,
        widget=forms.NumberInput(attrs={'placeholder': 'Enter debit amount'}),
    )


class CreditForm(forms.Form):
    amount = forms.IntegerField(
        label='Amount',
        min_value=1,
        widget=forms.NumberInput(attrs={'placeholder': 'Enter credit amount'}),
    )