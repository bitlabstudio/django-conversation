"""Forms for the ``conversation`` app."""
from django import forms
from django.contrib.auth.models import User

from .models import Conversation, Message


class MessageForm(forms.ModelForm):
    """Form to post new messages to a new or existing conversation."""
    def __init__(self, user, conversation, initial_user, *args, **kwargs):
        self.user = user
        self.conversation = conversation
        super(MessageForm, self).__init__(*args, **kwargs)
        if not self.conversation:
            users = User.objects.all()
            self.fields['recipients'] = forms.MultipleChoiceField(
                choices=[(u.pk, u) for u in users],
                initial=([initial_user.pk] if initial_user else ''),
            )
            self.fields['recipients'].hidden = True

    def save(self, *args, **kwargs):
        if not self.instance.pk:
            self.instance.user = self.user
            if not self.conversation:
                # Check for existing conversations of these users
                conversations = self.user.conversations.all()
                self.recipients = User.objects.filter(
                    pk__in=self.cleaned_data['recipients'])
                for user in self.recipients:
                    conversations = conversations.filter(
                        pk__in=user.conversations.values_list('pk'))
                if conversations:
                    self.conversation = conversations[0]
                else:
                    self.conversation = Conversation.objects.create()
                    self.conversation.users.add(self.user)
                    for user in self.recipients:
                        self.conversation.users.add(user)
            self.instance.conversation = self.conversation

            # Reset archive marks
            self.instance.conversation.archived_by.clear()
            # Reset reading status
            self.instance.conversation.read_by.clear()
        return super(MessageForm, self).save(*args, **kwargs).conversation

    class Meta:
        model = Message
        fields = ('text', )
