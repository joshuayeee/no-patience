from django.shortcuts import render

def login(request):
    return render(request, 'accounts/login/index.html')

def signup(request):
    return render(request, 'accounts/signup/index.html')

def forgot(request):
    return render(request, 'accounts/forgot-password/index.html')