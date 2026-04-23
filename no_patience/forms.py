from django import forms

from .models import Message

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['text']
        labels = {'text': ''}
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['text'].widget.attrs.update({'id': 'chatInput',
                                                 'class': 'chat-input-field',
                                                 'type': 'text',
                                                 'placeholder': "Type your message..."})
