from django.db import models
from django.contrib.auth.models import User, Group

class BankingUser(models.Model):      
    User_types = {
        'iu_re': 'Regular Employee',
        'iu_sm': 'System Manager',
        'iu_sa': 'System Administrator',
        'eu_cust': 'Customer',
        'eu_mo': 'Merchant/Organization',
    }

    modification_status = {
        'pending': 'Waiting for Approval',
        'rejected': 'Rejected',
        'approved': 'Approved'
    }

    requesting_deletion = {
        'yes': 'Yes',
        'no': 'No'
    }

    user = models.OneToOneField(User, on_delete = models.CASCADE, related_name = 'user')
    usertype = models.CharField(max_length = 256, choices = User_types)
    dob = models.DateField(default = None, blank = True, null = True)
    mobile_number = models.CharField(max_length = 256, default=None, blank=True, null = True)
    street_address = models.CharField(max_length = 512, default=None, blank=True, null = True)
    city = models.CharField(max_length = 128, default=None, blank=True, null = True)
    state = models.CharField(max_length = 128, default=None, blank=True, null = True)
    zip_code = models.CharField(max_length = 10, default=None, blank=True, null = True)
    country = models.CharField(max_length = 256, default=None, blank=True, null = True)
    account_created = models.DateTimeField(auto_now_add = True, null = True)
    user_handler = models.ForeignKey("BankingUser", on_delete = models.CASCADE, related_name = 'internal_user', blank=True, null = True)
    pd_modification_status = models.CharField(max_length = 128, choices = modification_status, blank=True, null = True)
    pd_modified = models.DateTimeField(auto_now = True, blank=True, null = True)
    deletion = models.CharField(max_length = 128, choices = requesting_deletion, blank=True, null = True, default = 'no')
    deletion_status = models.CharField(max_length = 128, choices = modification_status, blank=True, null = True)
    
    def __str__(self):
        return self.user.get_username() 


class Account(models.Model):
    account_types = {
        'sav': 'Savings Account',
        'check': 'Checking Account'
    }

    account_status = {
        'o': 'Open',
        'c': 'Close',
    }

    modification_status = {
       'pending': 'Waiting for approval',
       'rejected': 'Rejected',
       'approved': 'Approved'
    }


    account_number = models.AutoField(primary_key = True)
    account_type = models.CharField(max_length = 128, choices = account_types)
    banking_user = models.ForeignKey('BankingUser', on_delete = models.CASCADE, related_name = 'banking_user')
    account_bal = models.BigIntegerField(default = 0)
    created_on = models.DateTimeField(auto_now_add = True)
    account_status = models.CharField(max_length = 32, choices = account_status, default = 'o')
    closed_on = models.DateTimeField(blank = True, null = True)
    modification_status = models.CharField(max_length = 32, choices = modification_status, default = 'pending') 
 


    def __str__(self):
        return self.banking_user.user.first_name + '-' + self.account_type
    

class Transactions(models.Model):
    transaction_status = {
        'pending': 'Waiting for approval',
        'rejected': 'Rejected',
        'approved': 'Approved'
    }

    transaction_type = {
        'transfer': 'transfer',
        'credit': 'credit',
        'debit': 'debit'
    }

    otp_type={
        'yes':'yes',
        'no':'no'
    }

    from_account = models.ForeignKey('Account', on_delete = models.CASCADE, related_name = 'from_account')
    to_account = models.ForeignKey('Account', on_delete = models.CASCADE, related_name = 'to_account')
    amount = models.BigIntegerField()

    transaction_status = models.CharField(max_length = 128, choices = transaction_status)
    transaction_handler = models.ForeignKey(BankingUser, on_delete = models.CASCADE, related_name = 'transaction_handler')
    transaction_type= models.CharField(max_length = 128, choices = transaction_type,default = 'Error')
    initiated = models.DateTimeField(auto_now_add = True)
    status_changed = models.DateTimeField(auto_now = True)
    otp = models.BigIntegerField(default = 0)
    otp_verified = models.CharField(max_length = 128, choices = otp_type,default = 'No Action')

    def __str__(self):
        return str(self.from_account) + '-' + str(self.to_account)