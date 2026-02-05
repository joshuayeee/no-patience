from django.db import models

class Chat(models.Model):
    """Chat containing messages."""
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class UserMessage(models.Model):
    """Message sent by the user."""
    #my_chat = models.ForeignKey()
    text = models.TextField()
    date_sent = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.text[:50]}..."

class BotMessage(models.Model):
    """Message sent by the bot."""
    #my_chat = models.ForeignKey()
    text = models.TextField()
    date_sent = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.text[:50]}..."