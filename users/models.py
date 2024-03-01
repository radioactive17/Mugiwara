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

    user = models.OneToOneField(User, on_delete = models.CASCADE)
    user_type = models.CharField(max_length = 256, choices = User_types)
    dob = models.DateField(default = None, blank = True)
    mobile_number = models.CharField(max_length = 256, default=None, blank=True)
    street_address = models.CharField(max_length = 512, default=None, blank=True)
    city = models.CharField(max_length = 128, default=None, blank=True)
    state = models.CharField(max_length = 128, default=None, blank=True)
    zip_code = models.CharField(max_length = 10, default=None, blank=True)
    country = models.CharField(max_length = 256, default=None, blank=True)
    account_created = models.DateTimeField(auto_now_add = True)
    account_modified = models.DateTimeField(auto_now = True)


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
    account_type = models.CharField(max_length = 128, choices = account_types)
    user = models.ForeignKey('BankingUser', on_delete = models.CASCADE)
    account_bal = models.BigIntegerField(default = 0)
    created_on = models.DateTimeField(auto_now_add = True)
    account_status = models.CharField(max_length = 32, choices = account_status, default = 'o')
    closed_on = models.DateTimeField(blank = True, null = True)

    def __str__(self):
        return self.user.user.first_name + '-' + self.account_type
    

class Transactions(models.Model):
    transaction_status = {
        'pending': 'Waiting for approval',
        'rejected': 'Rejected',
        'approved': 'Approved'
    }

    from_account = models.ForeignKey('Account', on_delete = models.CASCADE, related_name = 'from_account')
    to_account = models.ForeignKey('Account', on_delete = models.CASCADE, related_name = 'to_account')
    amount = models.BigIntegerField()
    transaction_status = models.CharField(max_length = 128, choices = transaction_status)
    transaction_handler = models.ForeignKey(BankingUser, on_delete = models.CASCADE)
    initiated = models.DateTimeField(auto_now_add = True)
    status_changed = models.DateTimeField(auto_now = True)



