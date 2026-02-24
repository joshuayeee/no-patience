from django.shortcuts import render

from .models import Chat

def index(request):
    return render(request, 'no_patience/index.html')

def navbar(request):
    return render(request, 'no_patience/components/navbar.html')

def chat(request):
    return render(request, 'no_patience/components/chat.html')

def sidebar(request):
    """Display chats + allow creation of new chats."""
    chats = Chat.objects.order_by('date_added')
    context = {'chats': chats}
    return render(request, 'no_patience/components/sidebar.html', context)