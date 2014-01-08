"""Models for the conversation app."""
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Conversation(models.Model):
    """
    Model to contain different messages between one or more users.

    :users: Users participating in this conversation.
    :archived_by: List of participants, who archived this conversation.
    :read_by: List of participants, who read this conversation.

    """
    users = models.ManyToManyField(
        'auth.User',
        verbose_name=_('Users'),
        related_name='conversations',
    )

    archived_by = models.ManyToManyField(
        'auth.User',
        verbose_name=_('Archived by'),
        related_name='archived_conversations',
    )

    read_by = models.ManyToManyField(
        'auth.User',
        verbose_name=_('Read by'),
        related_name='read_conversations',
    )


class Message(models.Model):
    """
    Model, which holds information about a post within one conversation.

    :user: User, who posted the message.
    :conversation: Conversation, which contains this message.
    :date: Date the message was posted.
    :text: Message text.

    """
    user = models.ForeignKey(
        'auth.User',
        verbose_name=_('User'),
        related_name='messages',
    )

    conversation = models.ForeignKey(
        Conversation,
        verbose_name=_('Conversation'),
        related_name='messages',
    )

    date = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Date'),
    )

    text = models.TextField(
        max_length=2048,
        verbose_name=_('Text'),
    )
