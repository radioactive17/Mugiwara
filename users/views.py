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
from django.db.models import Sum
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Transactions, BankingUser


from .forms import DebitForm, CreditForm
from django.shortcuts import render, redirect
from .forms import Transactions_form

from .forms import Transactions_form
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
def view_account_approvals(request):
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
        return redirect('account-approvals')  # Redirect to the same page to display updated status
    
    return render(request, 'users/approve_registrations.html', {'registration_forms': registration_forms, 'user_types': user_types})

# ================================================ USER REGISTRATION / LOGIN ================================================



# ================================================ ACCOUNT CREATION ================================================
def create_account_view(request):
    return render(request, 'users/create_account_request.html')






# ================================================ ACCOUNT CREATION ================================================
@login_required
def profile(request):

    u = request.user
    banking_user = BankingUser.objects.get(user = u)
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance = request.user)
        b_form = BankingUserUpdateForm(request.POST, instance = banking_user)
        if u_form.is_valid() and b_form.is_valid():
            u_form.save()
            b_form.save()
            messages.success(request, 'Profile Updated Successfully')
            return redirect('profile')
    u_form = UserUpdateForm(instance = request.user)
    b_form = BankingUserUpdateForm(instance = banking_user)
    context = {
        'u_form': u_form,
        'b_form': b_form,
    }
    return render(request, 'users/profile.html', context)

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
        form = Transactions_form(request.POST)
        if form.is_valid():
            form.instance.transaction_status = 'pending'
            form.instance.transaction_handler = request.user.bankinguser
            form.save()
            return redirect('user_transactions')
    else:
        current_user_account = request.user.bankinguser.account_set.first()
        initial_data = {'from_account': current_user_account}
        form = Transactions_form(initial=initial_data)

    return render(request, 'users/create_transaction.html', {'form': form})




# can view all transactions
@login_required
def all_transactions(request):
   # Filter transactions where the current user is either the sender or the receiver
   transactions = Transactions.objects.all()


   return render(request, 'users/all_transactions.html', {'transactions': transactions})



# user view for all transactions
@login_required
def user_transactions(request):
   transactions = Transactions.objects.filter(
       Q(from_account__user=request.user.bankinguser) | Q(to_account__user=request.user.bankinguser)
   ).distinct()

   banking_user = request.user.bankinguser
   Account_user = Account.objects.get(user=banking_user)
   account_balance=Account_user.account_bal
   return render(request, 'users/user_transactions.html', {'transactions': transactions, 'account_balance': account_balance})



# user debit transaction
@transaction.atomic
def debit_view(request):
    form = DebitForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        amount = form.cleaned_data['amount']

        user = request.user.bankinguser
        account = Account.objects.get(user=user)

        if account.account_bal < amount:
            messages.error(request, "Insufficient funds.")
            return redirect('debit_view')

        # Deduct the amount from the account balance
        account.account_bal -= amount
        account.save()

        # Create a debit transaction record
        transaction_handler = BankingUser.objects.get(user=request.user)
        Transactions.objects.create(
            from_account=account,
            to_account=account,
            amount=amount,
            transaction_status='pending',
            transaction_handler=transaction_handler,
        )
        return redirect('/user_transactions')

    return render(request, 'users/debit_template.html', {'form': form})




# user credit transaction
@transaction.atomic
def credit_view(request):
    form = CreditForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        amount = form.cleaned_data['amount']

        user = request.user.bankinguser
        account = Account.objects.get(user=user)

        # Add the amount to the account balance
        account.account_bal += amount
        account.save()

        # Create a credit transaction record
        transaction_handler = BankingUser.objects.get(user=request.user)
        Transactions.objects.create(
            from_account=account,
            to_account=account,
            amount=amount,
            transaction_status='pending',
            transaction_handler=transaction_handler,
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



           # Perform deduction from "From_account"
           from_account = transaction.from_account
           from_account.account_bal -= transaction.amount
           to_account = transaction.to_account
           to_account.account_bal+=transaction.amount
           from_account.save()
           to_account.save()
           transaction.transaction_status = 'approved'
           transaction.transaction_handler = request.user.bankinguser
           transaction.save()


           # Perform additional actions if needed


           # Redirect or render a response as needed


   # Render a page for approving transactions (optional)
   return redirect('/all_transactions', transaction_id=transaction_id)



# Internal user decline transactions from users 
@login_required
def decline_transaction(request, transaction_id):
   transaction = get_object_or_404(Transactions, id=transaction_id)


   if request.method == 'POST':
       if transaction.transaction_status == 'pending':
       # Update the transaction status to 'rejected'
           transaction.transaction_status = 'rejected'
           transaction.transaction_handler = request.user.bankinguser
           transaction.save()


       # Redirect or render a response as needed


   # Render a page for declining transactions (optional)
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
    if transaction.transaction_status not in ['approved', 'declined']:
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

