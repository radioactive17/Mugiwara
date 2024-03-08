from django.contrib import admin
from django.urls import path
from . import views
from users.views import *
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

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
    path('account_approvals/', views.view_account_approvals, name = 'account-approvals')

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
