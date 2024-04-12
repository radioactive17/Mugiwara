from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from .models import *

# User Registration Form
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
    usertype = forms.ChoiceField(choices = User_types)
    user_approval = forms.ChoiceField(choices = user_approval)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password1', 'password2', 'usertype']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user_approval'] = forms.CharField(initial='pending', widget=forms.HiddenInput())

# Account Creation Form
class AccountCreationForm(ModelForm):
    class Meta:
        model = Account
        fields = ['banking_user', 'account_type', 'modification_status']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['modification_status'] = forms.CharField(initial='pending', widget=forms.HiddenInput())

# Account Approval Form
class AccountApprovalForm(ModelForm):
    class Meta:
        model = Account
        fields = ['banking_user', 'account_type', 'modification_status']
        # widgets = {
        #     'modification_status': forms.Select(choices=Account.modification_status.items())
        # }

    def __init__(self, *args, **kwargs):
        super(AccountApprovalForm, self).__init__(*args, **kwargs)
        self.fields['banking_user'].disabled = True
        self.fields['account_type'].disabled = True
        self.fields['modification_status'].label = "New Status for Account"
        self.fields['modification_status'].required = True


# BankingUser Deletion Request Form
class UserDeletionRequestForm(ModelForm):
    class Meta:
        model = BankingUser
        fields = ['deletion', 'deletion_status']

    def __init__(self, *args, **kwargs):
        super(UserDeletionRequestForm, self).__init__(*args, **kwargs)
        self.fields['deletion'].label = 'Are you sure you want to delete your profile?'
        self.fields['deletion_status'].initial = 'pending'
        self.fields['deletion_status'].widget = forms.HiddenInput()  # Hide the field
        # self.fields['deletion_status'].required = False  # Set the field as not required

# BankingUser Deletion Approval Form
class UserDeletionApprovalForm(ModelForm):
    class Meta:
        model = BankingUser
        fields = ['user', 'usertype', 'deletion_status']

    def __init__(self, *args, **kwargs):
        super(UserDeletionApprovalForm, self).__init__(*args, **kwargs)
        self.fields['user'].disabled = True
        self.fields['usertype'].disabled = True
        self.fields['deletion_status'].label = "Approve Deletion?"
        self.fields['deletion_status'].required = True

# User Update Form
class UserUpdateForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username']

    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        self.fields['username'].required = False
        self.fields['username'].disabled = True

# Banking User Form
class BankingUserUpdateForm(forms.Form):
    choices = {
        'pending': 'Pending',
        'approved': 'Approved',
        'rejected': 'Rejected',
    }

    first_name = forms.CharField(max_length = 256, required = False)
    last_name = forms.CharField(max_length = 256, required = False)
    username = forms.CharField(max_length = 256, required = False)
    dob = forms.DateField(required = False)
    mobile_number = forms.CharField(max_length = 256, required = False)
    street_address = forms.CharField(max_length = 512, required = False)
    city = forms.CharField(max_length = 128, required = False)
    state = forms.CharField(max_length = 128, required = False)
    zip_code = forms.CharField(max_length = 10, required = False)
    country = forms.CharField(max_length = 256, required = False)
    status = forms.ChoiceField(choices = choices, required = False)

    def __init__(self, *args, **kwargs):
        super(BankingUserUpdateForm, self).__init__(*args, **kwargs)
        self.fields['status'] = forms.CharField(initial='pending', widget=forms.HiddenInput())

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

class AccountDeletionRequestForm(ModelForm):
    class Meta:
        model = Account
        fields = ['account_type', 'modification_status']

    def __init__(self, user, *args, **kwargs):
        super(AccountDeletionRequestForm, self).__init__(*args, **kwargs)
        # Get unique account types for the user
        account_types = Account.objects.filter(banking_user=user).values_list('account_type', flat=True).distinct()
        # Create choices list
        choices = [(account_type, Account.account_types[account_type]) for account_type in account_types]
        # Set choices for account_type field
        self.fields['account_type'].choices = choices
        self.fields['modification_status'] = forms.CharField(initial='pending', widget=forms.HiddenInput())


from django import forms
from .models import Transactions, Account

class Transactions_Form(forms.ModelForm):
    class Meta:
        model = Transactions
        fields = ['to_account', 'amount']

    def __init__(self, *args, **kwargs):
        current_user = kwargs.pop('current_user', None)
        super().__init__(*args, **kwargs)

        # Exclude the current user's account from the options
        if current_user:
            self.fields['to_account'].queryset = Account.objects.exclude(banking_user=current_user)




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



class TransactionsForm(forms.ModelForm):
    class Meta:
        model = Transactions
        fields = ['amount']

from django import forms
from .models import PaymentRequest, BankingUser
from django.core.exceptions import ValidationError

class PaymentRequestForm(forms.ModelForm):
    client1 = forms.ModelChoiceField(queryset=BankingUser.objects.filter(usertype='eu_cust'))
    client2 = forms.ModelChoiceField(queryset=BankingUser.objects.filter(usertype='eu_cust'), required=False)

    class Meta:
        model = PaymentRequest
        fields = ['transaction_type', 'client1', 'client2', 'amount']

    # def __init__(self, *args, **kwargs):
    #     super(PaymentRequestForm, self).__init__(*args, **kwargs)
    #     self.fields['client1'].disabled = True
    #     self.fields['transaction_type'].disabled = True

    # def clean(self):
    #     cleaned_data = super().clean()
    #     transaction_type = cleaned_data.get('transaction_type')
    #     client2 = cleaned_data.get('client2')

    #     if transaction_type == 'transfer' and not client2:
    #         # Raise a ValidationError if transaction_type is 'transfer' and client2 is not provided
    #         self.add_error('client2', ValidationError("Client 2 is required for transfer transactions."))

    #     return cleaned_data

class OTPVerificationForm(forms.Form):
    otp = forms.CharField(max_length=6)

class UserModificationForm(forms.ModelForm):

    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)

    class Meta:
        model = BankingUser
        fields = ['first_name', 'last_name', 'mobile_number', 'street_address', 'city', 'state', 'zip_code', 'country']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(UserModificationForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial = user.last_name

class SelectUserForm(forms.Form):
    external_user = forms.ModelChoiceField(queryset=BankingUser.objects.filter(usertype='eu_cust'), label="Select User")

# class PaymentRequestForm(forms.ModelForm):
#     class Meta:
#         model = PaymentRequest
#         fields = ['from_client', 'to_client', 'amount']  # Ensure these fields exist in your model

#     def __init__(self, *args, **kwargs):
#         super(PaymentRequestForm, self).__init__(*args, **kwargs)
#         # Filter 'from_client' and 'to_client' to only include external individual users
#         self.fields['from_client'].queryset = BankingUser.objects.filter(usertype='eu_cust')
#         self.fields['to_client'].queryset = BankingUser.objects.filter(usertype='eu_cust')
