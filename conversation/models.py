"""Models for the conversation app."""
import os

from django.db import models
from django.conf import settings
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _


@python_2_unicode_compatible
class Conversation(models.Model):
    """
    Model to contain different messages between one or more users.

    :users: Users participating in this conversation.
    :archived_by: List of participants, who archived this conversation.
    :notified: List of participants, who have received an email notification.
    :unread_by: List of participants, who haven't read this conversation.
    :read_by_all: Date all participants have marked this conversation as read.

    """
    users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        verbose_name=_('Users'),
        related_name='conversations',
    )

    archived_by = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        verbose_name=_('Archived by'),
        related_name='archived_conversations',
        blank=True,
    )

    notified = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        verbose_name=_('Notified'),
        related_name='notified_conversations',
        blank=True,
    )

    unread_by = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        verbose_name=_('Unread by'),
        related_name='unread_conversations',
        blank=True,
    )

    read_by_all = models.DateTimeField(
        verbose_name=_('Read by all'),
        auto_now_add=True,
    )

    class Meta:
        ordering = ('-pk', )
        verbose_name = _('Conversation')
        verbose_name_plural = _('Conversations')

    def __str__(self):
        return '{}'.format(self.pk)

    def get_last_message(self):
        try:
            return self.messages.order_by('-date')[0]
        except IndexError:
            return None


@python_2_unicode_compatible
class Message(models.Model):
    """
    Model, which holds information about a post within one conversation.

    :user: User, who posted the message.
    :conversation: Conversation, which contains this message.
    :date: Date the message was posted.
    :text: Message text.

    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
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

    attachment = models.FileField(
        upload_to='conversation_messages',
        verbose_name=_('Attachment'),
        blank=True, null=True,
    )

    class Meta:
        ordering = ('-date', )
        verbose_name = _('Message')
        verbose_name_plural = _('Messages')

    def __str__(self):
        return self.user.email

    def filename(self):
        if self.attachment:  # pragma: nocover
            return os.path.basename(self.attachment.name)
        return ''


@python_2_unicode_compatible
class BlockedUser(models.Model):
    """
    Model to mark a user relationship as blocked.

    :user: Blocked user.
    :blocked_by: User who blocked the other one.
    :date: Date, the user has been blocked.

    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('Blocked user'),
        related_name='blocked',
    )

    blocked_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('Blocked by'),
        related_name='blocked_users',
    )

    date = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Date'),
    )

    class Meta:
        ordering = ('-date', )
        verbose_name = _('Blocked user')
        verbose_name_plural = _('Blocked users')

    def __str__(self):
        return self.user.email
