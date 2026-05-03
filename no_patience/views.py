from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404

from .models import Chat, Message
from .forms import MessageForm

import asyncio

from .llm import *

bot_message_text = ""

@login_required
def index(request):
    chats = Chat.objects.filter(owner=request.user).order_by("date_added")
    if (chats.count() > 0):
        chat = chats.first()
    else:
        chat = Chat.objects.create(name=f"New Chat", owner=request.user)
        chat.save()

    if chat.owner != request.user:
        raise Http404

    messages = chat.message_set.order_by('date_sent')

    message_form = MessageForm()

    context = {'chats': chats,
            'chat': chat,
            'messages': messages,
            'message_form': message_form}
    return render(request, 'no_patience/index.html', context)

@login_required
def reload(request, chat_id, new_chat_query=0):
    if (new_chat_query == 1):
        new_chat = Chat.objects.create(name=f"New Chat {Chat.objects.filter(owner=request.user).count() + 1}", owner=request.user)
        new_chat.save()
        return redirect(f"/reload/{new_chat.id}/0")
        
    chats = Chat.objects.filter(owner=request.user).order_by("date_added")
    chat = chats.get(id=chat_id)

    if chat.owner != request.user:
        raise Http404

    messages = chat.message_set.order_by('date_sent')

    if (request.method != 'POST'):
        message_form = MessageForm()
    else:
        message_form = MessageForm(data=request.POST)
        if message_form.is_valid():
            new_message = message_form.save(commit=False)
            new_message.my_chat = chat
            new_message.save()

            new_bot_message = Message.objects.create(
                my_chat=chat,
                text="",
                sent_by_bot=True
            )
            bot_message_text = f"This is message number {Message.objects.count()}"
            new_bot_message.text = bot_message_text
            new_bot_message.save()
            
            return redirect(f"/reload/{chat_id}/{new_chat_query}")

    context = {'chats': chats,
               'chat': chat,
               'messages': messages,
               'message_form': message_form}
    return render(request, 'no_patience/index.html', context)

"""
def generate_response(user_question):
    try:
        sql_query = generate_sql(user_question)

        if not is_safe_sql(sql_query):
            print("Unsafe or invalid query generated.")

        print("\nGenerated SQL:")
        print(sql_query)

        columns, rows = run_query(sql_query)

        print("\nRaw Result:")
        print(rows[:5])

        explanation = explain_result(user_question, columns, rows)

        print("Answer:")
        print(explanation)

        bot_message_text = explanation

    except errors.ClientError as e:
        if "429" in str(e):
            print("\n[Quota reached. retrying in 30 seconds...]")
            time.sleep(30)
        else:
            raise e
"""
"""
def generate():
    print("Ask a question about physicians (type 'exit' to quit)")

    while True:
        user_question = input(">> ")

        if user_question.lower() == "exit":
            break

        try:
            sql_query = generate_sql(user_question)

            if not is_safe_sql(sql_query):
                print("Unsafe or invalid query generated.")
                continue

            print("Generated SQL:")
            print(sql_query)

            columns, rows = run_query(sql_query)

            print("Raw Result:")
            print(rows[:5])

            explanation = explain_result(user_question, columns, rows)

            print("Answer:")
            print(explanation)

        except errors.ClientError as e:
            if "429" in str(e):
                print("\n[Quota reached. Retrying in 30 seconds...]")
                time.sleep(30)
            else:
                raise e
"""