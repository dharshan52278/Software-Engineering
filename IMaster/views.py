from django.shortcuts import render, redirect
from .models import *
# Create your views here.

def home(request):
    return render(request, "home.html")

def login(request):
    return render(request, "login.html")