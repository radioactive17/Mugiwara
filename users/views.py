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


def home(request):
    return render(request, 'users/home.html')


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            messages.info(request, f"You can SignIn once System Administrator approves your account")
            request.session['register_form'] = form.cleaned_data
            return redirect('login')
            if form.cleaned_data('user_approval') == 'approved':
                form.save()
                email_id = form.cleaned_data.get('email')
                messages.success(request, f'Welcome to Lappy Manage, {email_id}. You can now Log In using your set username and password')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'users/register.html', {'form':form})

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

@login_required
def view_account_approvals(request):
    form_data = request.session.pop('register_form')
    print(form_data)
    return render(request, 'users/account_approvals.html')