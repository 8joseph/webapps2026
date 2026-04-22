from django.urls import path
from . import views

urlpatterns = [
    path('<str:cur1>/<str:cur2>/<str:amount>/', views.conversion, name='conversion'),
]