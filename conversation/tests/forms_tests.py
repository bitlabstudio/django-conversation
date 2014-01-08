"""Tests for the forms of the ``conversation`` app."""
from django.test import TestCase

from django_libs.tests.factories import UserFactory

from .. import forms
from ..models import Conversation


class MessageFormTestCase(TestCase):
    """Tests for the ``MessageForm`` model."""
    longMessage = True

    def setUp(self):
        self.user = UserFactory()
        self.other_user = UserFactory()

    def test_form(self):
        data = {'text': 'Foo'}
        form = forms.MessageForm(user=self.user, conversation=None,
                                 data=data, initial_user=None)
        self.assertTrue(form.errors)
        self.assertFalse(form.is_valid())
        data.update({'recipients': ['999']})
        form = forms.MessageForm(user=self.user, conversation=None,
                                 data=data, initial_user=None)
        self.assertTrue(form.errors)
        self.assertFalse(form.is_valid())
        data.update({'recipients': ['{}'.format(self.other_user.pk)]})
        form = forms.MessageForm(user=self.user, conversation=None,
                                 data=data, initial_user=None)
        self.assertFalse(form.errors)
        self.assertTrue(form.is_valid())
        conversation = form.save()
        self.assertEqual(Conversation.objects.count(), 1, msg=(
            'A new conversation should\'ve been started with the message.'))
        form = forms.MessageForm(user=self.user, data=data,
                                 conversation=None, initial_user=None)
        form.cleaned_data = data
        form.save()
        self.assertEqual(Conversation.objects.count(), 1, msg=(
            'The existing conversation should\'ve been re-used.'))
        form = forms.MessageForm(user=self.user, data=data,
                                 conversation=conversation, initial_user=None)
        form.save()
        self.assertEqual(Conversation.objects.count(), 1, msg=(
            'The existing conversation should\'ve been re-used.'))
