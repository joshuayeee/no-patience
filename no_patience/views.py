from django.shortcuts import render

from .models import Chat
from .forms import ChatForm

def index(request):
    chats = Chat.objects.order_by("date_added")
    chat = Chat.objects.get(id=1)
    user_messages = chat.usermessage_set.order_by('-date_sent')
    bot_messages = chat.botmessage_set.order_by('-date_sent')
    context = {'chats': chats,
               'chat': chat,
               'user_messages': user_messages,
               'bot_messages': bot_messages}
    return render(request, 'no_patience/index.html', context)

def reload(request, chat_id):
    chats = Chat.objects.order_by("date_added")
    chat = Chat.objects.get(id=chat_id)
    user_messages = chat.usermessage_set.order_by('-date_sent')
    bot_messages = chat.botmessage_set.order_by('-date_sent')
    context = {'chats': chats,
               'chat': chat,
               'user_messages': user_messages,
               'bot_messages': bot_messages}
    return render(request, 'no_patience/index.html', context)

"""def navbar(request, chat_id):
    chat = Chat.objects.get(id=chat_id)
    context = {'chat': chat}
    return render(request, 'no_patience/components/navbar.html', context)

def chat(request, chat_id):
    chat = Chat.objects.get(id=chat_id)
    user_messages = chat.usermessage_set.order_by('-date_sent')
    bot_messages = chat.botmessage_set.order_by('-date_sent')
    context = {'chat': chat, 
               'user messages': user_messages, 
               'bot messages': bot_messages}
    return render(request, 'no_patience/components/chat.html', context)

def sidebar(request):
    chats = Chat.objects.order_by('date_added')
    context = {'chats': chats}
    return render(request, 'no_patience/components/sidebar.html', context)"""