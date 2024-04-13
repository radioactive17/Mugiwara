from urllib import request
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse
from .models import *
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from datetime import datetime
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator
from .forms import *
# views.py
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Transactions

from .forms import UserUpdateForm, BankingUserUpdateForm
from django.forms import formset_factory
from django.forms import modelformset_factory
from django.db.models import Sum
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Transactions, BankingUser




from .forms import DebitForm, CreditForm
from django.shortcuts import render, redirect


from .forms import Transactions_Form
from .models import Transactions
from django.db import transaction


from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings
from django.core.mail import send_mail




def home(request):
   return render(request, 'users/home.html')


# ================================================ USER REGISTRATION / LOGIN ================================================
def register(request):
   if request.method == 'POST':
       form = UserRegistrationForm(request.POST)
       if form.is_valid():
           registration_forms = request.session.get('registration_forms', [])
           registration_forms.append(form.cleaned_data)
           request.session['registration_forms'] = registration_forms
           messages.info(request, "Your registration request has been submitted for approval.")
           return redirect('login')
   else:
       form = UserRegistrationForm()
   return render(request, 'users/register.html', {'form':form})


# Send mail to user once account has been created or denied
@login_required
def user_approvals(request):
   registration_forms = request.session.get('registration_forms', [])
   user_types = UserRegistrationForm.User_types
   if request.method == 'POST':
       for form_data in registration_forms:
           print(form_data)
           status = request.POST.get(form_data['username'])
           if status  == 'approved' or status == 'rejected':
               if status == 'approved':
                   form_data['user_approval'] = request.POST.get(form_data['username'])
                   u = User(username = form_data['username'], first_name = form_data['username'], last_name = form_data['username'],
                            email = form_data['email'])
                   # user_type = form_data['user_type'], user_approval = form_data['user_approval']
                   u.set_password(form_data['password1'])
                   u.save()
                   bu = BankingUser(user = u, usertype = form_data['usertype'])
                   bu.save()
                   registration_forms.remove(form_data)


                   subject = 'Account Created Succesfully'
                   message = f"Hi {u.username}, thank you for registering in Mugiwara. You can now login using your username and password you created while registering"
                   email_from = settings.EMAIL_HOST_USER
                   recipient_list = [u.email, ]
                   send_mail( subject, message, email_from, recipient_list )


               elif status == 'rejected':
                   subject = 'Account Creation Denied'
                   message = f"Hi {form_data['username']}, thank you for registering in Mugiwara. Your account cannot be created, please contact bank manager for more details"
                   email_from = settings.EMAIL_HOST_USER
                   recipient_list = [form_data['email'], ]
                   send_mail( subject, message, email_from, recipient_list )
                   registration_forms.remove(form_data)
               else:
                   pass
       # Update session with modified registration_forms
       request.session['registration_forms'] = registration_forms
       return redirect('user-approvals')  # Redirect to the same page to display updated status

   return render(request, 'users/approve_registrations.html', {'registration_forms': registration_forms, 'user_types': user_types})


# ================================================ USER REGISTRATION / LOGIN ================================================




# ================================================ ACCOUNT CREATION ================================================
#Redirect here if no account
@login_required
def create_account(request):
   if request.method == 'POST':
       form = AccountCreationForm(request.POST)
       if form.is_valid():
        try:
            if Account.objects.get(banking_user = form.cleaned_data['banking_user'], account_type = form.cleaned_data['account_type'], modification_status = 'approved'):
                print('yes')
                messages.info(request, f'You already have this type of account. Please select a differnet account type')
            else:
                print('No account does not exist')
        except:
            print(form.cleaned_data)
            form.save()
            
            
   else:
       banking_user_instance = BankingUser.objects.get(user=request.user)
       form = AccountCreationForm(initial={'banking_user': banking_user_instance})


   return render(request, 'users/create_account_request.html', {'form': form})


@login_required
def approve_accounts(request):
   AccountApprovalFormSet = modelformset_factory(Account, form = AccountApprovalForm, extra = 0)
   formset = AccountApprovalFormSet(queryset = Account.objects.filter(modification_status = 'pending'))
   if request.method == 'POST':
       formset = AccountApprovalFormSet(request.POST or None)
       if formset.is_valid():
           for form in formset:
               if form.cleaned_data['modification_status'] == 'approved':
                   form.save()
               elif form.cleaned_data['modification_status'] == 'rejected':
                   a = Account.objects.get(banking_user = form.cleaned_data['banking_user'], account_type = form.cleaned_data['account_type'])
                   a.delete()
               else:
                   pass
   return render(request, 'users/account_approval.html', {'formset':formset})


# ================================================ ACCOUNT CREATION ================================================


# ================================================ PROFILE DELETION ================================================
@login_required
def request_profile_deletion(request, *args, **kwargs):
   if request.method == 'POST':
       form = UserDeletionRequestForm(request.POST, instance = BankingUser.objects.get(user = request.user))
       if form.is_valid():
           form.cleaned_data['deletion_status'] = 'pending'
           print(form.cleaned_data)
           messages.info(request, "Your request for Deletion has been submitted for approval")
           form.save()


           return redirect('mugiwara')
       else:
           print(form.errors)  # Print form errors for debugging
   else:
       form = UserDeletionRequestForm(instance = BankingUser.objects.get(user = request.user))
   return render(request, 'users/request_profile_deletion.html', {'form': form})


@login_required
def approve_profile_deletion(request, *args, **kwargs):
   UserDeletionFormSet = modelformset_factory(BankingUser, form = UserDeletionApprovalForm, extra = 0)
   formset = UserDeletionFormSet(queryset = BankingUser.objects.filter(deletion = 'yes'))
   if request.method == 'POST':
       formset = UserDeletionFormSet(request.POST or None)
       if formset.is_valid():
           for form in formset:
               print(form.cleaned_data)
               if form.cleaned_data['deletion_status'] == 'approved':
                   u = form.cleaned_data['user']
                   bu = BankingUser.objects.get(user = u)
                   bu.delete()
                   us = User.objects.get(username = u.username)
                   us.delete()
               elif form.cleaned_data['deletion_status'] == 'rejected':
                   u = form.cleaned_data['user']
                   bu = BankingUser.objects.get(user = u)
                   bu.deletion = 'no'
                   bu.save()
               else:
                   pass
           return redirect('mugiwara')
   return render(request, 'users/approve_profile_deletion.html', {'formset': formset})
# ================================================ PROFILE DELETION ================================================

# ------------------------------------------------------ PROFILE UPDATE ------------------------------------------------------
profile_update_requests = []
@login_required
def request_profile_update(request):
    banking_user_instance = BankingUser.objects.get(user=request.user)
    if request.method == 'POST':
        form = BankingUserUpdateForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            profile_update_requests.append({
                'user': request.user,
                'data': form.cleaned_data,
                'approved': False
            })
            messages.success(request, 'Your update request has been submitted for approval')
            # # Redirect to profile or any other appropriate URL after successful submission
        else:
            print(form.errors)
            # Handle form errors if needed
            # return render(request, 'users/profile.html', {'b_form': b_form})
    else:
        initial_data = {
            'first_name': banking_user_instance.user.first_name,
            'last_name': banking_user_instance.user.last_name,
            'username': banking_user_instance.user.username,
            'dob': banking_user_instance.dob,
            'mobile_number': banking_user_instance.mobile_number,
            'street_address': banking_user_instance.street_address,
            'city': banking_user_instance.city,
            'state': banking_user_instance.state,
            'zip_code': banking_user_instance.zip_code,
            'country': banking_user_instance.country,
        }
        form = BankingUserUpdateForm(initial=initial_data)
    context = {
        'form': form,
    }
    return render(request, 'users/profile_update.html', context)


def approve_profile_update(request):
    if request.method == 'POST':
        request_id = int(request.POST.get('request_id'))
        action = request.POST.get('action')
        print(request_id, action)
        if action == 'approve':
            user = User.objects.get(username = profile_update_requests[request_id]['user'])
            banking_user = BankingUser.objects.get(user = user)
            user.first_name = profile_update_requests[request_id]['data']['first_name']
            user.last_name = profile_update_requests[request_id]['data']['last_name']
            banking_user.dob = profile_update_requests[request_id]['data']['dob']
            banking_user.mobile_number = profile_update_requests[request_id]['data']['mobile_number']
            banking_user.street_address = profile_update_requests[request_id]['data']['street_address']
            banking_user.city = profile_update_requests[request_id]['data']['city']
            banking_user.state = profile_update_requests[request_id]['data']['state']
            banking_user.zip_code = profile_update_requests[request_id]['data']['zip_code']
            banking_user.country = profile_update_requests[request_id]['data']['country']
            user.save()
            banking_user.save()
            profile_update_requests.pop(int(request_id))
            messages.success(request, 'Request approved successfully.')
        elif action == 'reject':
            print('reject')
            # Code to reject request
            profile_update_requests.pop(int(request_id))
            messages.success(request, 'Request rejected successfully.')
        else:
            messages.error(request, 'Invalid action.')

    context = {
        'profile_update_requests': profile_update_requests,
    }
    return render(request, 'users/approve_profile_update.html', context)


# ------------------------------------------------------ PROFILE UPDATE ------------------------------------------------------

# ------------------------------------------------------ PROFILE VIEW ------------------------------------------------------
def profile(request):
    user = request.user
    banking_user = BankingUser.objects.get(user = user)
    context = {
        'user': user,
        'banking_user': banking_user,
    }
    return render(request, 'users/profile.html', context)

# ------------------------------------------------------ PROFILE VIEW ------------------------------------------------------

# ------------------------------------------------------ ACCOUNT VIEW ------------------------------------------------------
@login_required
def accounts(request):
    u = request.user
    banking_user = BankingUser.objects.get(user = u)
    accounts = Account.objects.filter(banking_user = banking_user)
    context = {
        'accounts': accounts,
    }
    return render(request, 'users/accounts.html', context)

# ------------------------------------------------------ ACCOUNT VIEW ------------------------------------------------------

# ------------------------------------------------------ ACCOUNT DELETE ------------------------------------------------------
# @login_required
# def accounts(request):
#    u = request.user
#    banking_user = BankingUser.objects.get(user = u)
#    account = Account.objects.filter(banking_user = banking_user)
#    if len(account) == 1:
#        account1 = account[0]
#        if request.method == 'POST':
#            a1_form = AccountUpdateForm(request.POST, instance = account1)
#            if a1_form.is_valid():
#                a1_form.save()
#                messages.success(request, 'Profile Updated Successfully')
#                return redirect('accounts')
#        a1_form = AccountUpdateForm(request.POST, instance = account1)
#        context = {
#            'a1_form': a1_form,
#        }
#        return render(request, 'users/accounts.html', context)
#    else:
#        account1 = account[0]
#        account2 = account[1]
#        if request.method == 'POST':
#            a1_form = AccountUpdateForm(request.POST, instance = account1)
#            a2_form = AccountUpdateForm(request.POST, instance = account2)
#            if a1_form.is_valid() and a2_form.is_valid():
#                a1_form.save()
#                a2_form.save()
#                messages.success(request, 'Accounts Updated Successfully')
#                return redirect('accounts')
#        a1_form = AccountUpdateForm(request.POST, instance = account1)
#        a2_form = AccountUpdateForm(request.POST, instance = account2)
#        context = {
#            'a1_form': a1_form,
#            'a2_form': a2_form,
#        }
#        return render(request, 'users/accounts.html', context)

account_delete_requests = []
def request_account_deletion(request):
    bu = BankingUser.objects.get(user = request.user)
    if request.method == 'POST':
        form = AccountDeletionRequestForm(bu, request.POST)
        if form.is_valid():
            # print(form.cleaned_data)
            account_delete_requests.append({
                'user': request.user,
                'data': form.cleaned_data,
                'approved': False
            })
            print(account_delete_requests)
            messages.success(request, 'Your request for account deletion has been submitted for approval')
    else:
        form = AccountDeletionRequestForm(bu)
    return render(request, 'users/request_account_deletion.html', {'form': form})

def approve_account_deletion(request):
    if request.method == 'POST':
        request_id = int(request.POST.get('request_id'))
        action = request.POST.get('action')
        print(request_id, action)
        if action == 'approve':
            user = User.objects.get(username = account_delete_requests[request_id]['user'])
            banking_user = BankingUser.objects.get(user = user)
            acc = Account.objects.get(banking_user = banking_user, account_type = account_delete_requests[request_id]['data']['account_type'])
            acc.delete()
            account_delete_requests.pop(int(request_id))
            messages.success(request, 'Deletion Request approved successfully.')
        elif action == 'reject':
            print('reject')
            account_delete_requests.pop(int(request_id))
            messages.info(request, 'Deletion Request rejected successfully.')
        else:
            messages.error(request, 'Invalid action.')
    context = {
        'account_delete_requests': account_delete_requests,
    }
    return render(request, 'users/approve_account_deletion.html', context)


# ------------------------------------------------------ ACCOUNT DELETE ------------------------------------------------------







@login_required
def debit(request, *args, **kwargs):
   return render(request, 'users/debit.html')


@login_required
def credit(request, *args, **kwargs):
   return render(request, 'users/credit.html')


@login_required
def view_accounts(request):
   users = User.objects.all()
   return render(request, 'users/view_accounts.html', {'users':users})


import random

def generate_otp(length=6):
    """Generate a random numeric OTP."""
    digits = [str(random.randint(0, 9)) for _ in range(length)]
    return ''.join(digits)


def send_otp_email(email, otp):
    subject = 'Your OTP for transaction confirmation'
    message = f'Your OTP for transaction confirmation is: {otp}'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list)


# User create transaction
@login_required
def create_transaction(request):
   if request.method == 'POST':
       form = Transactions_Form(request.POST)
       otp = generate_otp()
       if form.is_valid():
           user_pk = request.user.pk
           banking_user = BankingUser.objects.get(user_id=user_pk)
           form.instance.from_account =  Account.objects.get(banking_user=request.user.user)
           form.instance.transaction_status = 'pending'
           form.instance.transaction_handler = banking_user
           form.instance.transaction_type='transfer'
           form.instance.otp=otp
           form.save()
           send_otp_email(request.user.email, otp)
           transaction_id = form.instance.pk
           return redirect('verify_otp', transaction_id=transaction_id)
   else:
           user_pk = request.user.pk
           banking_user = BankingUser.objects.get(user_id=user_pk)
           current_user_account = Account.objects.get(banking_user=request.user.user)
           initial_data = {'from_account': current_user_account}
           form = Transactions_Form(initial=initial_data)

   return render(request, 'users/create_transaction.html', {'form': form})


@login_required
def verify_otp(request, transaction_id):
    transaction = Transactions.objects.get(pk=transaction_id)
    print(transaction)
    if request.method == 'POST':
        entered_otp = request.POST['otp']
        # print(type(transaction.otp))
        # print(type(entered_otp))
        # if int(transaction.otp) == int(entered_otp):
        #     print('SAME')
        # else:
        #     print('NOT SAME')
        if int(transaction.otp) == int(entered_otp):
            # OTP verified, confirm the transaction
            transaction.otp_verified='yes'
            transaction.save()
            messages.success(request, 'Transaction verified successfully.')
            return redirect('user_transactions')
        else:
            # Incorrect OTP entered
            return HttpResponse('<script>alert("Wrong OTP"); window.history.back();</script>')
    return render(request, 'users/verify_otp.html', {'transaction': transaction})





# can view all transactions
@login_required
def all_transactions(request):
  # Filter transactions where the current user is either the sender or the receiver
  transactions = Transactions.objects.all()
  payment_requests = PaymentRequest.objects.all()


  return render(request, 'users/all_transactions.html', {
        'transactions': transactions,
        'payment_requests': payment_requests
    })




from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponseRedirect
from .models import BankingUser, Transactions


@login_required
def user_transactions(request):
    user_pk = request.user.pk

    try:
        banking_user = BankingUser.objects.get(user__pk=user_pk)

        # Get the account balance for the user
        account_balance = Account.objects.filter(banking_user=banking_user).first().account_bal if Account.objects.filter(banking_user=banking_user).exists() else 0

        # Transactions where the user is either the sender or receiver
        user_transactions = Transactions.objects.filter(
            from_account__banking_user=banking_user
        ) | Transactions.objects.filter(
            to_account__banking_user=banking_user
        )
        user_transactions = user_transactions.order_by('-initiated')

        # Payment requests where the user is either client1 or client2
        payment_requests = PaymentRequest.objects.filter(
            client1=banking_user
        ) | PaymentRequest.objects.filter(
            client2=banking_user
        )
        payment_requests = payment_requests.order_by('-id')

        context = {
            'transactions': user_transactions,
            'account_balance': account_balance,
            'payment_requests': payment_requests,
        }

        return render(request, 'users/user_transactions.html', context)

    except BankingUser.DoesNotExist:
        messages.error(request, "Something went wrong.")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))








# user debit transaction
@transaction.atomic
def debit_view(request):
   form = DebitForm(request.POST or None)


   if request.method == 'POST' and form.is_valid():
       amount = form.cleaned_data['amount']


       user_pk = request.user.pk
       banking_user = BankingUser.objects.get(user_id=user_pk)
       account = Account.objects.get(banking_user=banking_user)


       if account.account_bal < amount:
           messages.error(request, "Insufficient funds.")
           return redirect('debit_view')

       otp = generate_otp()
       # Deduct the amount from the account balance
       # account.account_bal -= amount
       # account.save()


       # Create a debit transaction record
       transaction_handler = BankingUser.objects.get(user=request.user)
       transaction=Transactions.objects.create(
           from_account=account,
           to_account=account,
           amount=amount,
           transaction_status='pending',
           transaction_handler=transaction_handler,
           transaction_type='debit',
           otp=otp
       )
       send_otp_email(request.user.email, otp)
       return redirect('verify_otp', transaction_id=transaction.pk)


   return render(request, 'users/debit_template.html', {'form': form})








# user credit transaction
@transaction.atomic
def credit_view(request):
   form = CreditForm(request.POST or None)


   if request.method == 'POST' and form.is_valid():
       amount = form.cleaned_data['amount']
       user_pk = request.user.pk
       banking_user = BankingUser.objects.get(user_id=user_pk)
       account = Account.objects.get(banking_user=banking_user)


       # Add the amount to the account balance
       # account.account_bal += amount
       # account.save()
       otp = generate_otp()

       # Create a credit transaction record
       transaction_handler = BankingUser.objects.get(user=request.user)
       transaction=Transactions.objects.create(
           from_account=account,
           to_account=account,
           amount=+amount,
           transaction_status='pending',
           transaction_handler=transaction_handler,
           transaction_type='credit',
           otp=otp,
       )


       send_otp_email(request.user.email, otp)
       return redirect('verify_otp', transaction_id=transaction.pk)


   return render(request, 'users/credit_template.html', {'form': form})





from django.http import HttpResponseForbidden


# Internal user approve transactions from users
@login_required
# users/views.py
def approve_transaction(request, transaction_id):
  transaction = get_object_or_404(Transactions, id=transaction_id)




  if request.method == 'POST':
    if transaction.transaction_status == 'pending' and transaction.otp_verified == 'yes':
          # Update the transaction status to 'approved'
           if transaction.transaction_type == 'transfer':
          # Perform deduction from "From_account" and add to "To_account"

                from_account = transaction.from_account
                from_account.account_bal -= transaction.amount
                if from_account.account_bal<0:
                    return HttpResponse('<script>alert("Cannot approve. Account does not have sufficient funds."); window.history.back();</script>')
                to_account = transaction.to_account
                to_account.account_bal+=transaction.amount
                from_account.save()
                to_account.save()


           elif transaction.transaction_type == 'credit':
                from_account= transaction.from_account
                from_account.account_bal +=transaction.amount
                from_account.save()


           elif transaction.transaction_type == 'debit':
                from_account= transaction.from_account
                from_account.account_bal -=transaction.amount
                if from_account.account_bal<0:
                    return HttpResponse('<script>alert("Cannot approve. Account does not have sufficient funds."); window.history.back();</script>')
                from_account.save()

           else:
               return HttpResponse('<script>alert("Cannot approve. Transaction Type is Error"); window.history.back();</script>')

           transaction.transaction_status = 'approved'
           user_pk = request.user.pk
           banking_user = BankingUser.objects.get(user_id=user_pk)
           transaction.transaction_handler = banking_user
           transaction.save()
    else:
        return HttpResponse('<script>alert("OTP verification is Incomplete"); window.history.back();</script>')



  return redirect('/all_transactions', transaction_id=transaction_id)






# Internal user decline transactions from users
@login_required
def decline_transaction(request, transaction_id):
  transaction = get_object_or_404(Transactions, id=transaction_id)




  if request.method == 'POST':
      if transaction.transaction_status == 'pending':
      # Update the transaction status to 'rejected'
          transaction.transaction_status = 'rejected'
          user_pk = request.user.pk
          banking_user = BankingUser.objects.get(user_id=user_pk)
          transaction.transaction_handler = banking_user
          transaction.save()


  return redirect('/all_transactions', transaction_id=transaction_id)






from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from .forms import TransactionsForm  # Import your form
from django.urls import reverse
from django.shortcuts import redirect


@login_required
def modify_transaction(request, transaction_id):
   transaction = get_object_or_404(Transactions, id=transaction_id)


   # Check if the transaction status is neither approved nor declined
   if transaction.transaction_status not in ['approved', 'rejected']:
       # Process modification logic here


       # For example, you can create a form instance and render a template
       form = TransactionsForm(instance=transaction)


       # Handle form submission
       if request.method == 'POST':
           form = TransactionsForm(request.POST, instance=transaction)
           if form.is_valid():
               form.save()
               return redirect('all_transactions') # Use the name of the URL pattern


       return render(request, 'users/modify_transaction.html', {'form': form, 'transaction': transaction})
   else:
       # If the transaction is approved or declined, redirect to a page indicating it cannot be modified
       return HttpResponse('<script>alert("Cannot modify. Transaction is already approved or declined."); window.history.back();</script>')


from django.shortcuts import render
from .models import *
from django.http import HttpResponseForbidden


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import PaymentRequestForm
from .models import PaymentRequest, BankingUser


@login_required
def submit_payment_request(request):
    if request.method == 'POST':
        form = PaymentRequestForm(request.POST)
        if form.is_valid():
            payment_request = form.save(commit=False)
            # Retrieve the BankingUser instance associated with the logged-in User
            # Use request.user.user due to the unconventional related_name='user'
            payment_request.merchant = request.user.user
            payment_request.otp = generate_otp()
            payment_request.save()

            send_otp_email(payment_request.client1.user.email, payment_request.otp)
            return redirect('verify_payment_otp', payment_request_id=payment_request.id)
    else:
        form = PaymentRequestForm()
    return render(request, 'users/submit_payment_request.html', {'form': form})


@login_required
def verify_payment_otp(request, payment_request_id):
    payment_request = get_object_or_404(PaymentRequest, id=payment_request_id)
    if request.method == 'POST':
        form = OTPVerificationForm(request.POST)
        if form.is_valid() and payment_request.otp == form.cleaned_data['otp']:
            payment_request.otp_verified = True
            payment_request.awaiting_internal_approval = True  # Indicate it's awaiting internal approval
            payment_request.save()
            messages.success(request, 'OTP verified successfully. Your payment request is pending internal approval.')
            return redirect('merchant_transaction_history')
        else:
            messages.error(request, 'Incorrect OTP. Please try again.')
    else:
        form = OTPVerificationForm()
    return render(request, 'users/verify_payment_otp.html', {'form': form, 'payment_request': payment_request})


from django.db import transaction as db_transaction


@login_required
def approve_payment_request(request, request_id):
    payment_request = get_object_or_404(PaymentRequest, id=request_id)

    if payment_request.status == 'pending' and payment_request.otp_verified:
        if request.method == 'POST':
            # critical_transaction_amount = 10000

            # if payment_request.amount > critical_transaction_amount and request.user.banking_user.usertype != 'iu_sm':
            #     messages.error(request, "Only system managers can authorize critical transactions over USD 10,000.")
            #     return redirect('all_transactions')

            client1_accounts = payment_request.client1.banking_user.all()  # Use the 'banking_user' related_name
            if client1_accounts.exists():
                client1_account = client1_accounts.first()  # Assuming client1 has at least one account

                if payment_request.transaction_type == 'deposit':
                    client1_account.account_bal += payment_request.amount
                    client1_account.save()

                elif payment_request.transaction_type == 'withdraw':
                    if client1_account.account_bal >= payment_request.amount:
                        client1_account.account_bal -= payment_request.amount
                        client1_account.save()
                    else:
                        messages.error(request, "Insufficient funds in the account for withdrawal.")
                        return redirect('all_transactions')

                elif payment_request.transaction_type == 'transfer' and payment_request.client2:
                    client2_accounts = payment_request.client2.banking_user.all()  # Use the 'banking_user' related_name
                    if client2_accounts.exists():
                        client2_account = client2_accounts.first()  # Assuming client2 has at least one account
                        if client1_account.account_bal >= payment_request.amount:
                            client1_account.account_bal -= payment_request.amount
                            client2_account.account_bal += payment_request.amount
                            client1_account.save()
                            client2_account.save()
                        else:
                            messages.error(request, "Insufficient funds in the account for transfer.")
                            return redirect('all_transactions')

                payment_request.status = 'approved'
                payment_request.save()

                messages.success(request, "Payment request approved successfully.")
                return redirect('all_transactions')
            else:
                messages.error(request, "Client1 does not have an account.")
                return redirect('all_transactions')
    else:
        messages.error(request, "This payment request cannot be approved or OTP is not verified.")

    return redirect('all_transactions')

@login_required
def decline_payment_request(request, request_id):
    payment_request = get_object_or_404(PaymentRequest, id=request_id)

    # Ensure that only pending requests can be declined
    if payment_request.status == 'pending':
        if request.method == 'POST':
            payment_request.status = 'declined'
            payment_request.save()
            messages.success(request, 'Payment request declined.')
            return redirect('all_transactions')  # Adjust the redirect as needed
        else:
            # Show a confirmation page for GET requests
            return render(request, 'users/decline_payment_request.html', {'payment_request': payment_request})
    else:
        messages.error(request, 'This payment request cannot be declined.')
        return redirect('users/all_transactions')  # Adjust the redirect as needed


@login_required
def modify_payment_request(request, request_id):
    payment_request = get_object_or_404(PaymentRequest, id=request_id)
    if payment_request.status == 'pending':
        form = PaymentRequestForm(request.POST or None, instance=payment_request)
        if request.method == 'POST':
            if form.is_valid():
                form.save()
                messages.success(request, 'Payment request modified successfully.')
                return redirect('all_transactions')
            else:
                # Log or print form errors to debug
                print(form.errors)
                messages.error(request, 'Please correct the errors below.')
        return render(request, 'users/modify_payment_request.html', {'form': form, 'payment_request': payment_request})
    else:
        messages.error(request, "Modification is not allowed. Payment request is already approved or declined.")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


@login_required
def modify_payment_request_amount(request, request_id):

    payment_request = get_object_or_404(PaymentRequest, id=request_id)

    if payment_request.merchant.user != request.user:
        messages.error(request, "You do not have permission to modify this payment request.")
        return redirect('merchant_transaction_history')

    if payment_request.status != 'pending':
        messages.error(request, 'This payment request cannot be modified.')
        return redirect('merchant_transaction_history')

    if request.method == 'POST':
        payment_request = get_object_or_404(PaymentRequest, id=request_id, merchant=request.user.user)
        new_amount = request.POST.get('new_amount')

        # Perform necessary validation on new_amount if required

        payment_request.amount = new_amount
        payment_request.save()

        messages.success(request, 'Transaction amount updated successfully.')
        return redirect('merchant_transaction_history')

@login_required
def merchant_transaction_history(request):
    # Access the BankingUser instance associated with the logged-in User
    banking_user = request.user.user

    if banking_user.usertype != 'eu_mo':
        return HttpResponseForbidden('You are not authorized to view this page.')

    merchant_payment_requests = PaymentRequest.objects.filter(merchant=banking_user)

    context = {
        'payment_requests': merchant_payment_requests,
    }

    return render(request, 'users/merchant_transaction_history.html', context)

@login_required
def modify_user_personal_data(request):
    if request.method == 'POST':
        form = SelectUserForm(request.POST)
        if form.is_valid():
            selected_user_id = form.cleaned_data['external_user'].id
            return redirect('modify_user_details', user_id=selected_user_id)
    else:
        form = SelectUserForm()
    return render(request, 'users/modify_user_personal_data.html', {'form': form})

@login_required
def modify_user_details(request, user_id):
    banking_user = get_object_or_404(BankingUser, pk=user_id)
    user_instance = banking_user.user  # Assuming a ForeignKey to Django's User model

    initial_data = {
        'first_name': user_instance.first_name,
        'last_name': user_instance.last_name,
        'mobile_number': banking_user.mobile_number,
        'street_address': banking_user.street_address,
        'city': banking_user.city,
        'state': banking_user.state,
        'zip_code': banking_user.zip_code,
        'country': banking_user.country,
    }

    if request.method == 'POST':
        form = UserModificationForm(request.POST, initial=initial_data)
        if form.is_valid():
            user_instance.first_name = form.cleaned_data['first_name']
            user_instance.last_name = form.cleaned_data['last_name']
            # Save any other User model fields as needed
            user_instance.save()

            # Now update the BankingUser instance
            banking_user.mobile_number = form.cleaned_data['mobile_number']
            banking_user.street_address = form.cleaned_data['street_address']
            banking_user.city = form.cleaned_data['city']
            banking_user.state = form.cleaned_data['state']
            banking_user.zip_code = form.cleaned_data['zip_code']
            banking_user.country = form.cleaned_data['country']
            # Save any other BankingUser fields as needed
            banking_user.save()

            # Create a modification request for approval
            modification_data = form.cleaned_data.copy()
            modification_data.pop('first_name', None)
            modification_data.pop('last_name', None)
            # Remove any other non-BankingUser fields as needed

            UserModificationRequest.objects.create(
                requested_by=request.user,
                user_to_modify=banking_user,
                data=modification_data
            )

            # Redirect or show success message
            return redirect('/')  # Update this to your actual success URL
    else:
        form = UserModificationForm(initial=initial_data)

    return render(request, 'users/modify_user_details.html', {'form': form, 'banking_user': banking_user})


from django.contrib import messages
from django.db import transaction

@login_required
def approve_modifications(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden('Unauthorized')

    if request.method == 'POST':
        request_id = request.POST.get('request_id')
        decision = request.POST.get('decision')
        modification_request = get_object_or_404(UserModificationRequest, id=request_id)

        with transaction.atomic():
            if decision == 'approve':
                modification_request.status = 'approved'
                # Apply the modifications to the BankingUser instance
                user_to_modify = modification_request.user_to_modify
                for field, value in modification_request.data.items():
                    setattr(user_to_modify, field, value)
                user_to_modify.save()
                messages.success(request, f'Modification request for {user_to_modify} approved.')

            elif decision == 'decline':
                modification_request.status = 'declined'
                messages.info(request, f'Modification request for {user_to_modify} declined.')

            modification_request.save()

    modification_requests = UserModificationRequest.objects.filter(status='pending')
    return render(request, 'users/approve_modifications.html', {'modification_requests': modification_requests})

# @login_required
# def create_payment_request(request):
#     if request.method == 'POST':
#         form = PaymentRequestForm(request.POST, user=request.user)
#         if form.is_valid():
#             payment_request = form.save(commit=False)
#             payment_request.merchant = BankingUser.objects.get(user=request.user)

#             # Generate and assign OTP
#             otp = generate_otp()
#             payment_request.otp = otp
#             payment_request.save()

#             # Send OTP to Client1's email
#             send_otp_email(payment_request.client1.user.email, otp)

#             # Redirect to OTP verification page, passing the ID of the newly created payment request
#             return redirect('verify_otp', transaction_id=payment_request.id)
#     else:
#         form = PaymentRequestForm(user=request.user)

#     return render(request, 'users/create_payment_request.html', {'form': form})

# from django.views.decorators.cache import never_cache


# @never_cache
# @login_required
# def verify_merchant_payment_otp(request, payment_request_id):
#     payment_request = get_object_or_404(PaymentRequest, id=payment_request_id, merchant__user=request.user)

#     if request.method == 'POST':
#         entered_otp2 = request.POST['otp'] # Strip whitespace

#         # Ensure both OTPs are strings for comparison, log values for debugging
#         stored_otp = str(payment_request.otp)
#         print(f"Verifying OTP: Stored OTP='{payment_request.otp}', Entered OTP='{entered_otp2}'")


#         if int(payment_request.otp) == int(entered_otp2):
#             payment_request.otp_verified = 'yes'
#             payment_request.status = 'approved'  # Adjust according to your application logic
#             payment_request.save()
#             messages.success(request, 'Payment request verified successfully.')
#             return redirect('merchant_dashboard')  # Redirect to the desired URL
#         else:
#             messages.error(request, 'Incorrect OTP. Please try again.')

#     return render(request, 'users/verify_merchant_payment_otp.html', {'payment_request': payment_request})

# @login_required
# def approve_payment_request(request, request_id):
#     payment_request = get_object_or_404(PaymentRequest, id=request_id, client1__user=request.user)

#     if request.method == 'POST':
#         if 'approve' in request.POST:
#             payment_request.status = 'approved'
#             # Implement logic to process the payment here
#         elif 'reject' in request.POST:
#             payment_request.status = 'rejected'
#         payment_request.save()
#         return redirect('payment_approval_success')

#     return render(request, 'users/approve_payment_request.html', {'payment_request': payment_request})

@login_required
def merchant_dashboard(request):
    if not request.user.userprofile.is_merchant:  # Assuming you have a way to identify merchant users
        return HttpResponseForbidden('Access Denied')

    payment_requests = PaymentRequest.objects.filter(merchant=request.user)
    return render(request, 'merchant_dashboard.html', {'payment_requests': payment_requests})

# @login_required
# def payment_requests_status(request):
#     if request.user.user.usertype != 'eu_mo':
#         return HttpResponseForbidden('Access Denied')

#     payment_requests = PaymentRequest.objects.filter(merchant__user=request.user)
#     return render(request, 'users/payment_requests_status.html', {'payment_requests': payment_requests})



# from django.core.mail import send_mail
# from django.conf import settings



# @login_required
# def merchant_dashboard(request):
#     if request.user.user.usertype != 'eu_mo':
#         return HttpResponseForbidden("You are not authorized to view this page.")

#     accounts = Account.objects.filter(banking_user=request.user.user)
#     payment_requests = PaymentRequest.objects.filter(merchant=request.user.user)
#     recent_transactions = Transactions.objects.filter(from_account__in=accounts).order_by('-initiated')[:5]

#     context = {
#         'accounts': accounts,
#         'payment_requests': payment_requests,
#         'recent_transactions': recent_transactions,
#     }
#     return render(request, 'users/merchant_dashboard.html', context)

# from django import forms
# from .models import PaymentRequest

# class PaymentRequestForm(forms.ModelForm):
#     class Meta:
#         model = PaymentRequest
#         fields = ['client_name', 'amount', 'description']

# from django.core.mail import send_mail
# from django.urls import reverse
# from django.contrib.auth.decorators import login_required
# from django.http import HttpResponseForbidden
# from django.shortcuts import render, redirect
# from .forms import *
# from .models import PaymentRequest


# @login_required
# def submit_payment_request(request):
#     if request.user.user.usertype != 'eu_mo':
#         return HttpResponseForbidden("You are not authorized to access this page.")

#     if request.method == 'POST':
#         form = PaymentSubmissionForm(request.POST)
#         if form.is_valid():
#             payment_request = form.save(commit=False)
#             payment_request.merchant = request.user.user  # Set the current merchant as the requester
#             payment_request.status = 'pending'
#             payment_request.save()
#             # Redirect to a confirmation page or the dashboard
#             return redirect('merchant_dashboard')
#     else:
#         form = PaymentSubmissionForm()

#     return render(request, 'users/submit_payment_request.html', {'form': form})


# @login_required
# def submit_payment_request(request):
#     if request.user.user.usertype != 'eu_mo':
#         return HttpResponseForbidden("You are not authorized to access this page.")

#     if request.method == 'POST':
#         form = PaymentSubmissionForm(request.POST)
#         if form.is_valid():
#             payment_request = form.save(commit=False)
#             payment_request.merchant = request.user.user  # Set the current merchant as the requester
#             payment_request.status = 'pending'
#             payment_request.save()

#             # Construct the authorization URL
#             auth_url = request.build_absolute_uri(reverse("authorize_payment_request", args=[payment_request.id]))

#             # Send the authorization email to the from_client
#             send_mail(
#                 'Payment Request Authorization',
#                 f'Please authorize the payment request by clicking on the link: {auth_url}',
#                 {settings.DEFAULT_FROM_EMAIL},  # Replace with your actual email
#                 [payment_request.from_client.user.email],  # Ensure from_client has a related user with an email
#                 fail_silently=False,
#             )

#             # Redirect to a confirmation page or the dashboard
#             return redirect('merchant_dashboard')
#     else:
#         form = PaymentSubmissionForm()

#     return render(request, 'users/submit_payment_request.html', {'form': form})

# from django.http import HttpResponseForbidden, HttpResponseNotFound

# @login_required
# def client_dashboard(request):
#     if request.user.user.usertype != 'eu_cust':
#         return HttpResponseForbidden("You are not authorized to access this page.")

#     pending_requests = PaymentRequest.objects.filter(from_client=request.user.user, status='pending')

#     return render(request, 'users/client_dashboard.html', {'pending_requests': pending_requests})



# @login_required
# def authorize_payment_request(request, payment_request_id):
#     try:
#         payment_request = PaymentRequest.objects.get(id=payment_request_id, from_client=request.user.user, status='pending')
#     except PaymentRequest.DoesNotExist:
#         return HttpResponseNotFound("Payment request not found or you're not authorized to view this page.")

#     if request.method == 'POST':
#         payment_request.status = 'authorized'
#         payment_request.save()
#         # Redirect to a confirmation page, the client's dashboard, or a success message
#         return redirect('client_dashboard')  # Make sure to define this URL

#     return render(request, 'users/authorize_payment_request.html', {'payment_request': payment_request})

# # from django.core.mail import send_mail
# # from django.urls import reverse





# @login_required
# def create_payment_request(request):
#     if request.method == 'POST':
#         form = PaymentRequestForm(request.POST)
#         if form.is_valid():
#             payment_request = form.save(commit=False)
#             payment_request.merchant = request.user.user
#             payment_request.status = 'pending'
#             payment_request.save()
#             return redirect('merchant_dashboard')
#     else:
#         form = PaymentRequestForm()

#     return render(request, 'users/create_payment_request.html', {'form': form})


# @login_required
# def view_payment_requests(request):
#     if request.user.user.usertype != 'eu_mo':
#         return HttpResponseForbidden("You are not authorized to access this page.")

#     payment_requests = PaymentRequest.objects.filter(merchant=request.user.user)

#     return render(request, 'users/payment_requests.html', {'payment_requests': payment_requests})

from django.shortcuts import render
from django.core.mail import send_mail
from .forms import ContactForm
from django.conf import settings

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            
            # Sending email
            send_mail(
                'Contact Us Form Submission',
                f'Name: {name}\nEmail: {email}\nMessage: {message}',
                settings.DEFAULT_FROM_EMAIL,
                [settings.CONTACT_EMAIL],  # Change to your contact email
                fail_silently=False,
            )
            # return render(request, 'contact_success.html')
            return redirect('base.html')  # Create a success page
    else:
        form = ContactForm()
    return render(request, 'users/contact_form.html', {'form': form})