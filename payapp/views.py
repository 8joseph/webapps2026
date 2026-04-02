from django.shortcuts import render
from django.views.decorators.cache import never_cache


@never_cache    #dont cache so user cannot logout and return to logged in pag
def home(request):
    return render(request, 'index.html')