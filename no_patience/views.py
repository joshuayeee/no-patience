from django.shortcuts import render

def index(request):
    return render(request, 'no_patience/index.html')