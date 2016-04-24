"""Tests for the models of the ``conversation`` app."""
from django.test import TestCase

from mixer.backend.django import mixer


class BlockedUserTestCase(TestCase):
    """Tests for the ``BlockedUser`` model."""
    longMessage = True

    def setUp(self):
        self.blocked = mixer.blend('conversation.BlockedUser')

    def test_model(self):
        self.assertTrue(str(self.blocked), msg=(
            'Should be able to instantiate and save the object.'))


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

    def test_filename(self):
        self.assertEqual(self.message.filename(), '', msg=(
            'Should return an empty string, if there is no file attached.'))
