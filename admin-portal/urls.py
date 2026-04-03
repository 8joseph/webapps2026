from django.urls import path

from . import views

urlpatterns = [
    path('accounts/',views.admin_accounts,name='admin_accounts'),
    path('new-admin/', views.register_new_admin,name='register_admin'),
    path('admin-transactions/',views.admin_transactions,name='admin_transactions'),
]