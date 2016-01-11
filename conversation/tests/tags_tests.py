"""Tests for the template tag of the ``conversation`` app."""
from django.contrib.auth.models import User
from django.test import TestCase

from mixer.backend.django import mixer

from ..templatetags import conversation_tags


class ChainUserNamesTestCase(TestCase):
    """Tests for the ``chain_user_names`` template filter."""
    longMessage = True

    def test_tag(self):
        user1 = mixer.blend('auth.User')
        user2 = mixer.blend('auth.User')
        self.assertEqual(
            conversation_tags.chain_user_names([], user1),
            '', msg=('Should return an empty string, if the list is empty.'))
        self.assertEqual(
            conversation_tags.chain_user_names(
                User.objects.all(), user1),
            user2.username,
            msg=('Should return chained profile names.'))


class IsBlockedTestCase(TestCase):
    """Tests for the ``is_blocked`` template filter."""
    longMessage = True

    def test_tag(self):
        self.assertFalse(conversation_tags.is_blocked('foo', 'bar'))
        user1 = mixer.blend('auth.User')
        user2 = mixer.blend('auth.User')
        self.assertFalse(conversation_tags.is_blocked(user1, user2))
        mixer.blend('conversation.BlockedUser', blocked_by=user1, user=user2)
        self.assertTrue(conversation_tags.is_blocked(user1, user2))
