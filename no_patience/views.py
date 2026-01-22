from django.shortcuts import render

def index(request):
    return render(request, 'no_patience/index.html')

def navbar(request):
    return render(request, 'no_patience/components/navbar.html')

def chat(request):
    return render(request, 'no_patience/components/chat.html')

def sidebar(request):
    return render(request, 'no_patience/components/sidebar.html')