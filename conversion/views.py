from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
# Create your views here.


CURRENCIES = ('EUR', 'USD', 'GBP')
#conversion rates as of 22/04/2026
CONVERSIONS = {
    'EUR': {
        'USD': 1.17,
        'GBP': 0.86,
    },
    'USD': {
        'EUR': 0.85,
        'GBP': 0.74,
    },
    'GBP': {
        'EUR': 1.15,
        'USD': 1.35,
    }
}

@api_view(['GET'])
def conversion(request, cur1, cur2, amount):
    try:
        amount = float(amount)
        if cur1 in CURRENCIES and cur2 in CURRENCIES:
            if cur1 == cur2:
                converted_amount = amount
                rate = 1.0
            else:
                rate = CONVERSIONS[cur1][cur2]
                converted_amount = amount * rate
            return Response({'amount' : converted_amount, 'conversion_rate' : rate}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid currency code'}, status=status.HTTP_400_BAD_REQUEST)
    except ValueError:
        return Response({'error': 'Invalid amount'}, status=status.HTTP_400_BAD_REQUEST)
