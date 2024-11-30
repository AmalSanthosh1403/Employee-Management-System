from django.shortcuts import render
from .models import *

def login_regFuntion(request):
    return render(request,'login_reg.html')