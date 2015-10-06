"""Forms for the ``conversation`` app."""
from django import forms

from .models import Conversation, Message


class MessageForm(forms.ModelForm):
    """Form to post new messages to a new or existing conversation."""
    def __init__(self, user, conversation, initial_user, *args, **kwargs):
        self.user = user
        self.conversation = conversation
        self.initial_user = initial_user
        super(MessageForm, self).__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        if not self.instance.pk:
            self.instance.user = self.user
            if not self.conversation:
                self.conversation = Conversation.objects.create()
                self.conversation.users.add(*[self.user, self.initial_user])
            self.instance.conversation = self.conversation

            # Reset archive marks
            self.instance.conversation.archived_by.clear()
            # Reset reading status
            self.instance.conversation.read_by.clear()
        return super(MessageForm, self).save(*args, **kwargs).conversation

    class Meta:
        model = Message
        fields = ('text', 'attachment')
