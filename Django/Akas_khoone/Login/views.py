from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse


def login_view(request):
    username = request['username']
    password = request['password']
    user = authenticate(request, username=username, password=password)

    if user is not None:
        login(request, user)
        return JsonResponse({'err':'0'})
    else:
        return JsonResponse({'err':'1', 'errlog':'username or pass is wrong'})



