"""Tests for the models of the ``conversation`` app."""
from django.test import TestCase

from .factories import ConversationFactory, MessageFactory


class ConversationTestCase(TestCase):
    """Tests for the ``Conversation`` model."""
    longMessage = True

    def setUp(self):
        self.conversation = ConversationFactory()

    def test_model(self):
        self.assertTrue(self.conversation.pk, msg=(
            'Should be able to instantiate and save the object.'))


class MessageTestCase(TestCase):
    """Tests for the ``Message`` model."""
    longMessage = True

    def setUp(self):
        self.message = MessageFactory()

    def test_model(self):
        self.assertTrue(self.message.pk, msg=(
            'Should be able to instantiate and save the object.'))
