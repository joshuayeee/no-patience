from django.shortcuts import render, redirect

from .models import Chat, Message
from .forms import MessageForm

def index(request):
    chats = Chat.objects.order_by("date_added")
    chat = Chat.objects.get(id=1)
    messages = chat.message_set.order_by('date_sent')

    message_form = MessageForm()

    context = {'chats': chats,
               'chat': chat,
               'messages': messages,
               'message_form': message_form}
    return render(request, 'no_patience/index.html', context)

def reload(request, chat_id, new_chat_query=0):
    if (new_chat_query == 1):
        new_chat = Chat.objects.create(name=f"New Chat {Chat.objects.count() + 1}")
        new_chat.save()
        return redirect(f"/reload/{new_chat.id}/0")
        
    chats = Chat.objects.order_by("date_added")
    chat = Chat.objects.get(id=chat_id)
    messages = chat.message_set.order_by('date_sent')

    if (request.method != 'POST'):
        message_form = MessageForm()
    else:
        message_form = MessageForm(data=request.POST)
        if message_form.is_valid():
            new_message = message_form.save(commit=False)
            new_message.my_chat = chat
            new_message.save()
            return redirect(f"/reload/{chat_id}/{new_chat_query}")

    context = {'chats': chats,
               'chat': chat,
               'messages': messages,
               'message_form': message_form}
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