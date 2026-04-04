from . import views
from django.urls import path

urlpatterns = [
    path('', views.home, name='home'),
    path('accept-transaction/<int:transaction_id>/', views.accept_transaction_request, name='accept_transaction'),
    path('decline-transaction/<int:transaction_id>/', views.decline_transaction_request, name='decline_transaction'),
]