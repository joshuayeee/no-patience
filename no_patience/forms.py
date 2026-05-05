from django import forms

from .models import Message

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['text']
        labels = {'text': ''}
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['text'].widget = forms.Textarea(attrs={
            'id': 'chatInput',
            'class': 'chat-input-field',
            'placeholder': 'Type your message...',
            'rows': 1,
        })