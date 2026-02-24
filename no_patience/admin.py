from django.contrib import admin

from .models import UserMessage, Chat, BotMessage

admin.site.register(UserMessage)
admin.site.register(Chat)
admin.site.register(BotMessage)