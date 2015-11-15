"""Tests for the forms of the ``conversation`` app."""
from django.test import TestCase

from mixer.backend.django import mixer

from .. import forms
from ..models import Conversation


class MessageFormTestCase(TestCase):
    """Tests for the ``MessageForm`` model."""
    longMessage = True

    def setUp(self):
        self.user = mixer.blend('auth.User')
        self.other_user = mixer.blend('auth.User')

    def test_form(self):
        data = {'text': 'Foo'}
        form = forms.MessageForm(user=self.user, conversation=None, data=data,
                                 initial_user=self.other_user)
        self.assertFalse(form.errors)
        self.assertTrue(form.is_valid())
        conversation = form.save()
        self.assertEqual(Conversation.objects.count(), 1, msg=(
            'A new conversation should\'ve been started with the message.'))
        form = forms.MessageForm(user=self.user, data=data, initial_user=None,
                                 conversation=conversation)
        form.save()
        self.assertEqual(Conversation.objects.count(), 1, msg=(
            'The existing conversation should\'ve been re-used.'))

        blocked_user = mixer.blend('conversation.BlockedUser',
                                   blocked_by=self.user, user=self.other_user)
        form = forms.MessageForm(user=self.user, data=data, initial_user=None,
                                 conversation=conversation)
        self.assertTrue(form.errors, msg=(
            'Conversation should have been blocked'))

        blocked_user.delete()
        mixer.blend('conversation.BlockedUser',
                    user=self.user, blocked_by=self.other_user)
        form = forms.MessageForm(user=self.user, data=data, initial_user=None,
                                 conversation=conversation)
        self.assertTrue(form.errors, msg=(
            'Conversation should have been blocked'))
