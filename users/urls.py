from django.contrib import admin
from django.urls import path
from . import views
from users.views import *
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from .views import all_transactions


urlpatterns = [
   path('', views.home, name = 'mugiwara'),
   path('register/', views.register, name = 'signup'),
   path('login/', auth_views.LoginView.as_view(template_name = 'users/login.html'), name = 'login'),
   path('logout/', auth_views.LogoutView.as_view(), {'next_page': settings.LOGOUT_REDIRECT_URL},  name = 'logout'),
   path('profile/', views.profile, name = 'profile'),
   path('accounts/', views.accounts, name = 'accounts'),
   path('debit/<int:pk>', views.debit, name = 'debit'),
   path('credit/<int:pk>/', views.credit, name = 'credit'),

   path('view_accounts/', views.view_accounts, name = 'view-accounts'),
   path('account_approvals/', views.view_account_approvals, name = 'account-approvals'),


   path('', views.home, name = 'mugiwara'),
   path('login/', auth_views.LoginView.as_view(template_name = 'users/login.html'), name = 'login'),
   path('logout/', auth_views.LogoutView.as_view(), {'next_page': settings.LOGOUT_REDIRECT_URL},  name = 'logout'),
   path('profile', views.profile, name = 'profile'),
   path('all_transactions', views.all_transactions, name='all_transactions'),
   path('approve_transaction/<int:transaction_id>', views.approve_transaction, name='approve_transaction'),
   path('decline_transaction/<int:transaction_id>', views.decline_transaction, name='decline_transaction'),
   path('user_transactions',views.user_transactions,name='user_transactions'),
   path('create_transaction', create_transaction, name='create_transaction'),
   path('debit', debit_view, name='debit_view'),
   path('credit', credit_view, name='credit_view'),
   path('modify_transaction/<int:transaction_id>/', modify_transaction, name='modify_transaction'),

]

if settings.DEBUG:
   urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)


