"""
URL configuration for webapps2026 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from register import views as register_view
from payapp import views as payapp_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('payapp.urls'),name='home'),
    path('register/', register_view.register_user, name='register'),
    path('login/', register_view.login_user, name='login'),
    path('logout/', register_view.logout_user, name='logout'),
    path('admin-portal/', include('admin-portal.urls')),
    path('new-transaction/', payapp_views.new_transaction, name='new_transaction'),
    path('request-transaction/', payapp_views.request_transaction, name='request_transaction'),
    path('transactions/', payapp_views.user_transactions, name='user-transactions'),
    path('payapp/', include('payapp.urls')),
]
