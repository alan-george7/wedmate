# site_admin/urls.py
from django.urls import path
from .views import *

urlpatterns = [
    path('login/', admin_login, name='admin_login'),
    path('logout/', admin_logout, name='admin_logout'),
    path('dashboard/', admin_dashboard, name='admin_dashboard'),
    path('user-accounts/', user_accounts, name='admin_user_accounts'),
    path('vendor-accounts/', vendor_accounts, name='admin_vendor_accounts'),
    path('delete-vendor/<int:vendor_id>/', delete_vendor, name='delete_vendor'),
]
