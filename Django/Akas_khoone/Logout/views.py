from django.shortcuts import render
from django.contrib.auth import authenticate, logout

def logout_view(request):
    logout(request)
