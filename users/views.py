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
           form.save()
           return redirect('mugiwara')
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
    return render(request, 'users/profile.html', context)

# def approve_profile_update(request, *args, **kwargs):
#     if request.method == 'POST':
#         for key, value in request.POST.items():
#             print(key, value)
#         # request_index = int(request.POST.get('request_index'))
#         # action = request.POST.get('status')
#         # if action == 'approved':
#         #     print('approved')
#         #     # profile_update_requests[request_index]['approved'] = True
#         #     # messages.success(request, 'Profile update request approved successfully.')
#         # elif action == 'rejected':
#         #     print('denied')
#             # del profile_update_requests[request_index]
#             # messages.error(request, 'Profile update request denied.')

#         # return redirect('profile_update_requests')

#     context = {
#         'update_requests': profile_update_requests,
#     }
#     return render(request, 'users/approve_profile_update.html', context)

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

@login_required
def accounts(request):
   u = request.user
   banking_user = BankingUser.objects.get(user = u)
   account = Account.objects.filter(banking_user = banking_user)
   if len(account) == 1:
       account1 = account[0]
       if request.method == 'POST':
           a1_form = AccountUpdateForm(request.POST, instance = account1)
           if a1_form.is_valid():
               a1_form.save()
               messages.success(request, 'Profile Updated Successfully')
               return redirect('accounts')
       a1_form = AccountUpdateForm(request.POST, instance = account1)
       context = {
           'a1_form': a1_form,
       }
       return render(request, 'users/accounts.html', context)
   else:
       account1 = account[0]
       account2 = account[1]
       if request.method == 'POST':
           a1_form = AccountUpdateForm(request.POST, instance = account1)
           a2_form = AccountUpdateForm(request.POST, instance = account2)
           if a1_form.is_valid() and a2_form.is_valid():
               a1_form.save()
               a2_form.save()
               messages.success(request, 'Accounts Updated Successfully')
               return redirect('accounts')
       a1_form = AccountUpdateForm(request.POST, instance = account1)
       a2_form = AccountUpdateForm(request.POST, instance = account2)
       context = {
           'a1_form': a1_form,
           'a2_form': a2_form,
       }
       return render(request, 'users/accounts.html', context)






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




# User create transaction
@login_required
def create_transaction(request):
   if request.method == 'POST':
       form = Transactions_Form(request.POST)
       if form.is_valid():
           user_pk = request.user.pk
           banking_user = BankingUser.objects.get(user_id=user_pk)
           form.instance.from_account =  Account.objects.get(banking_user=request.user.user)
           form.instance.transaction_status = 'pending'
           form.instance.transaction_handler = banking_user
           form.instance.transaction_type='transfer'
           form.save()
           return redirect('user_transactions')
   else:
           user_pk = request.user.pk
           banking_user = BankingUser.objects.get(user_id=user_pk)
           current_user_account = Account.objects.get(banking_user=request.user.user)
           initial_data = {'from_account': current_user_account}
           form = Transactions_Form(initial=initial_data)




   return render(request, 'users/create_transaction.html', {'form': form})








# can view all transactions
@login_required
def all_transactions(request):
  # Filter transactions where the current user is either the sender or the receiver
  transactions = Transactions.objects.all()


  return render(request, 'users/all_transactions.html', {'transactions': transactions})




from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponseRedirect
from .models import BankingUser, Transactions


def user_transactions(request):
   # Get the primary key (pk) of the currently logged-in user
   user_pk = request.user.pk


   try:
       # Get the associated BankingUser instance
       banking_user = BankingUser.objects.get(user_id=user_pk)


       # Get the account balance for the user
       Account_user = Account.objects.get(banking_user=banking_user)
       account_balance=Account_user.account_bal
       # Filter transactions where the user is either the sender or receiver
       user_transactions = Transactions.objects.filter(
           from_account__banking_user_id=user_pk
       ) | Transactions.objects.filter(
           to_account__banking_user_id=user_pk
       )


       # You might want to order the transactions by date or ID
       user_transactions = user_transactions.order_by('-initiated')


       return render(request, 'users/user_transactions.html', {'transactions': user_transactions, 'account_balance': account_balance})


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


       # Deduct the amount from the account balance
       # account.account_bal -= amount
       # account.save()


       # Create a debit transaction record
       transaction_handler = BankingUser.objects.get(user=request.user)
       Transactions.objects.create(
           from_account=account,
           to_account=account,
           amount=amount,
           transaction_status='pending',
           transaction_handler=transaction_handler,
           transaction_type='debit',
       )
       return redirect('/user_transactions')


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


       # Create a credit transaction record
       transaction_handler = BankingUser.objects.get(user=request.user)
       Transactions.objects.create(
           from_account=account,
           to_account=account,
           amount=+amount,
           transaction_status='pending',
           transaction_handler=transaction_handler,
           transaction_type='credit',
       )




       return redirect('/user_transactions')


   return render(request, 'users/credit_template.html', {'form': form})








# Internal user approve transactions from users
@login_required
# users/views.py
def approve_transaction(request, transaction_id):
  transaction = get_object_or_404(Transactions, id=transaction_id)




  if request.method == 'POST':
      if transaction.transaction_status == 'pending':
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







