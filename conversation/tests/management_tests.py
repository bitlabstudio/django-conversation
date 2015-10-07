"""Tests for the management commands `send_message_digest`."""
from django.core import mail
from django.core.management import call_command
from django.test import TestCase
from django.utils.timezone import now, timedelta

from mixer.backend.django import mixer


class SendMessageDigestTestCase(TestCase):
    longMessage = True

    def test_validates_and_saves_input(self):
        two_days_ago = now() - timedelta(days=2)
        user = mixer.blend('auth.User')
        conversation = mixer.blend('conversation.Conversation')
        conversation.users.add(user)
        conversation.unread_by.add(user)
        call_command('send_message_digest')
        self.assertEqual(len(mail.outbox), 0, msg=(
            'No digest should have been sent.'))
        conversation.read_by_all = two_days_ago
        conversation.save()
        call_command('send_message_digest')
        self.assertEqual(len(mail.outbox), 1, msg=(
            'One digest should have been sent.'))
