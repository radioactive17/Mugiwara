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
    
    
    

