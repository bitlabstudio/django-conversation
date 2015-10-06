"""Tests for the models of the ``conversation`` app."""
from django.test import TestCase

from mixer.backend.django import mixer


class ConversationTestCase(TestCase):
    """Tests for the ``Conversation`` model."""
    longMessage = True

    def setUp(self):
        self.conversation = mixer.blend('conversation.Conversation')

    def test_model(self):
        self.assertTrue(str(self.conversation), msg=(
            'Should be able to instantiate and save the object.'))


class MessageTestCase(TestCase):
    """Tests for the ``Message`` model."""
    longMessage = True

    def setUp(self):
        self.message = mixer.blend('conversation.Message')

    def test_model(self):
        self.assertTrue(str(self.message), msg=(
            'Should be able to instantiate and save the object.'))
