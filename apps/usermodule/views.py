
# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return render(request, 'bookmodule/index.html')

def index2(request, val1=0): 
    return HttpResponse("value1 = " + str(val1))