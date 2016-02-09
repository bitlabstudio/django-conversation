"""Forms for the ``conversation`` app."""
from django import forms
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _

from . import models


class MessageForm(forms.ModelForm):
    """Form to post new messages to a new or existing conversation."""
    def __init__(self, user, conversation, initial_user, *args, **kwargs):
        self.user = user
        self.initial_user = initial_user
        self.conversation = conversation
        if self.conversation:
            conversation_users = self.conversation.users.all()
        else:
            conversation_users = [self.initial_user]
        # Check if this conversation has been blocked
        self.blocked_users = models.BlockedUser.objects.filter(
            Q(blocked_by=self.user, user__in=conversation_users) |
            Q(user=self.user, blocked_by__in=conversation_users),
        )
        super(MessageForm, self).__init__(*args, **kwargs)

    def clean(self):
        if self.blocked_users and self.blocked_users.filter(
                blocked_by=self.user):
            raise forms.ValidationError(_(
                'You have blocked this conversation.'))
        elif self.blocked_users:
            raise forms.ValidationError(_('You have been blocked.'))
        return super(MessageForm, self).clean()

    def save(self, *args, **kwargs):
        if not self.instance.pk:
            self.instance.user = self.user
            if self.conversation:
                self.instance.conversation = self.conversation
            else:
                self.instance.conversation = \
                    models.Conversation.objects.create()
                self.instance.conversation.users.add(
                    *[self.user, self.initial_user])

            # Reset archive marks
            self.instance.conversation.archived_by.clear()
            # Mark as unread
            self.instance.conversation.unread_by.add(
                *self.instance.conversation.users.exclude(pk=self.user.pk))
            # Clear notification note
            self.instance.conversation.notified.clear()
        return super(MessageForm, self).save(*args, **kwargs).conversation

    class Meta:
        model = models.Message
        fields = ('text', 'attachment')
