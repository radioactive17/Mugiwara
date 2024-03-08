from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from .models import *


class UserRegistrationForm(UserCreationForm):
    user_approval = {
       'pending': 'Waiting for approval',
       'rejected': 'Rejected',
       'approved': 'Approved'
    }

    User_types = {
        'eu_cust': 'Customer',
        'eu_mo': 'Merchant/Organization',
        'iu_re': 'Employee',
        'iu_sm': 'System Manager',
        'iu_sa': 'System Administrator',
    }

    email = forms.EmailField()
    user_type = forms.ChoiceField(choices = User_types)
    user_approval = forms.ChoiceField(choices = user_approval)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password1', 'password2', 'user_type']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user_approval'] = forms.CharField(initial='pending', widget=forms.HiddenInput())

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
        exclude = ['user', 'user_handler', 'pd_modification_status']
        
    def __init__(self, *args, **kwargs):
        super(BankingUserUpdateForm, self).__init__(*args, **kwargs)

        if self.instance.id:
            self.fields['user_type'].disabled = True
            
    
class AccountUpdateForm(ModelForm):
    class Meta:
        model = Account
        fields = ['account_number', 'account_type', 'account_bal', 'account_status']
        # fields = '__all__'
        # exclude = ['user', 'closed_on']
    
    def __init__(self, *args, **kwargs):
        super(AccountUpdateForm, self).__init__(*args, **kwargs)

        if self.instance.account_number:
            self.fields['account_type'].disabled = True
            self.fields['account_bal'].disabled = True
            self.fields['account_status'].disabled = True


