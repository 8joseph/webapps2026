from django.urls import path

from . import views

urlpatterns = [
    path('accounts/',views.admin_accounts,name='admin_accounts'),
    path('new-admin/', views.register_new_admin,name='register_admin'),
]