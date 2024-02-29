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