from django.db import models

class Chat(models.Model):
    """Chat containing messages."""
    name = models.CharField(max_length=50)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class UserMessage(models.Model):
    """User's messages sent in a chat."""
    my_chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    text = models.TextField()
    date_sent = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.text[:50]}..."

class BotMessage(models.Model):
    """Bot's messages sent in a chat."""
    my_chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    text = models.TextField()
    date_sent = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.text[:50]}..."