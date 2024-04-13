from django.contrib import admin
from django.urls import path
from . import views
from users.views import *
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from .views import all_transactions
from .views import *


urlpatterns = [
   path('', views.home, name = 'mugiwara'),
   path('register/', views.register, name = 'signup'),
   path('login/', auth_views.LoginView.as_view(template_name = 'users/login.html'), name = 'login'),
   path('logout/', auth_views.LogoutView.as_view(), {'next_page': settings.LOGOUT_REDIRECT_URL},  name = 'logout'),
   path('accounts/', views.accounts, name = 'accounts'),
   path('debit/<int:pk>', views.debit, name = 'debit'),
   path('credit/<int:pk>/', views.credit, name = 'credit'),

   path('view_accounts/', views.view_accounts, name = 'view-accounts'),
   path('profile/', views.profile, name = 'profile'),
   # Approve User Registration
   path('user_approvals/', views.user_approvals, name = 'user-approvals'),
   # Create Account
   path('create_account/', views.create_account, name = 'create-account'),
   path('account_approvals/', views.approve_accounts, name = 'account-approvals'),
   # Delete Profile
   path('profile_deletion/', views.request_profile_deletion, name = 'profile-deletion'),
   path('approve_profile_deletion/', views.approve_profile_deletion, name = 'approve-profile-deletion'),
   # Update Profile
   path('update_profile/', views.request_profile_update, name = 'update-profile'),
   path('profile_approvals/', views.approve_profile_update, name = 'profile-approvals'),
   # Delete Account
   path('delete_account/', views.request_account_deletion, name = 'account-delete'),
   path('approve_account_deletion/', views.approve_account_deletion, name = 'approve-account-deletion'),

   path('all_transactions', views.all_transactions, name='all_transactions'),
   path('approve_transaction/<int:transaction_id>/', approve_transaction, name='approve_transaction'),
   path('decline_transaction/<int:transaction_id>', views.decline_transaction, name='decline_transaction'),
   path('user_transactions',views.user_transactions,name='user_transactions'),
   path('create_transaction', create_transaction, name='create_transaction'),
   path('verify_otp/<int:transaction_id>/', views.verify_otp, name='verify_otp'),
   path('debit', debit_view, name='debit_view'),
   path('credit', credit_view, name='credit_view'),
   path('modify_transaction/<int:transaction_id>/', modify_transaction, name='modify_transaction'),

   path('submit_payment_request/', submit_payment_request, name='submit_payment_request'),
   path('verify_payment_otp/<int:payment_request_id>/', verify_payment_otp, name='verify_payment_otp'),
   path('merchant_dashboard/', merchant_dashboard, name='merchant_dashboard'),
   path('decline_payment_request/<int:request_id>/', views.decline_payment_request, name='decline_payment_request'),
   path('modify_payment_request/<int:request_id>/', views.modify_payment_request, name='modify_payment_request'),
   path('approve_payment_request/<int:request_id>/', views.approve_payment_request, name='approve_payment_request'),
   path('merchant_transaction_history/', views.merchant_transaction_history, name='merchant_transaction_history'),
   path('modify_payment_request_amount/<int:request_id>/', modify_payment_request_amount, name='modify_payment_request_amount'),

   path('modify_user_personal_data/', views.modify_user_personal_data, name='modify_user_personal_data'),
   path('modify_user_details/<int:user_id>/', views.modify_user_details, name='modify_user_details'),
   path('approve_modifications/', views.approve_modifications, name='approve_modifications'),
   # path('contact/', contact, name='contact'),



   # path('create_payment_request/', views.create_payment_request, name='create_payment_request'),
   # path('payment_requests_status/', views.payment_requests_status, name='payment_requests_status'),
   # path('approve_payment_request/<int:request_id>/', views.approve_payment_request, name='approve_payment_request'),
   # path('verify_merchant_payment_otp/<int:payment_request_id>/', views.verify_merchant_payment_otp, name='verify_merchant_payment_otp'),




   # path('merchant/dashboard/', merchant_dashboard, name='merchant_dashboard'),
   # path('payment/request/new/', views.create_payment_request, name='create_payment_request'),


   # path('payment_requests/', views.view_payment_requests, name='view_payment_requests'),
   # path('submit_payment_request/', views.submit_payment_request, name='submit_payment_request'),

   # path('authorize_payment/<int:payment_request_id>/', views.authorize_payment_request, name='authorize_payment_request'),
   # path('client/dashboard/', views.client_dashboard, name='client_dashboard'),


   path('forgot_password/', views.forgot_password, name='forgot_password'),
   path('reset_password/', views.reset_password, name='reset_password'),
   path('change_password/<str:token>/', views.change_password, name='change_password'),


]

if settings.DEBUG:
   urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)


