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
from .forms import UserUpdateForm, BankingUserUpdateForm
# users/views.py


from django.shortcuts import render, get_object_or_404, redirect


from .models import Transactions


from django.db.models import Q




def home(request):
   # laptopo = LaptopO.objects.all().order_by('-laptop_id')[:12]
   # context = {
   #      'laptopo': laptopo,
   #  }
  
   return render(request, 'users/home.html')




# class UpdateBankingUserView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
#     model = BankingUser
#     form_class = BankingUserUpdateForm
#     success_message = 'Details updated successfully'
  
#     def test_func(self):
#         if self.request.user.is_authenticated:
#             return True
#         return False
  
#     def get_object(self, *args, **kwargs):
#         return BankingUser.objects.get(user = self.kwargs['pk'])


#     def get_success_url(self):
#         return reverse("profile", kwargs={"pk": self.kwargs['pk']})




@login_required
def profile(request):
   if request.method == 'POST':
       u_form = UserUpdateForm(request.POST, instance = request.user)
       b_form = BankingUserUpdateForm(request.POST, instance = request.user.bankinguser)
       if u_form.is_valid() and b_form.is_valid():
           u_form.save()
           b_form.save()
           messages.success(request, 'Profile Updated Successfully')
           return redirect('profile')
   u_form = UserUpdateForm(instance = request.user)
   b_form = BankingUserUpdateForm(instance = request.user.bankinguser)


   context = {
       'u_form': u_form,
       'b_form': b_form,
   }
   return render(request, 'users/profile.html', context)


@login_required
def all_transactions(request):
   # Filter transactions where the current user is either the sender or the receiver
   transactions = Transactions.objects.filter(
       Q(from_account__user=request.user.bankinguser) | Q(to_account__user=request.user.bankinguser)
   ).distinct()


   return render(request, 'users/all_transactions.html', {'transactions': transactions})




@login_required
def user_transactions(request):
   transactions = Transactions.objects.filter(
       Q(from_account__user=request.user.bankinguser) | Q(to_account__user=request.user.bankinguser)
   ).distinct()


   return render(request, 'users/user_transactions.html', {'transactions': transactions})


@login_required
# users/views.py
def approve_transaction(request, transaction_id):
   transaction = get_object_or_404(Transactions, id=transaction_id)


   if request.method == 'POST':
       if transaction.transaction_status == 'pending':
           # Update the transaction status to 'approved'
           transaction.transaction_status = 'approved'


           # Perform deduction from "From_account"
           from_account = transaction.from_account
           from_account.account_bal -= transaction.amount
           from_account.save()


           transaction.save()


           # Perform additional actions if needed


           # Redirect or render a response as needed


   # Render a page for approving transactions (optional)
   return redirect('/user_transactions', transaction_id=transaction_id)




@login_required
def decline_transaction(request, transaction_id):
   transaction = get_object_or_404(Transactions, id=transaction_id)


   if request.method == 'POST':
       if transaction.transaction_status == 'pending':
       # Update the transaction status to 'rejected'
           transaction.transaction_status = 'rejected'
           transaction.save()


       # Redirect or render a response as needed


   # Render a page for declining transactions (optional)
   return redirect('/user_transactions', transaction_id=transaction_id)


