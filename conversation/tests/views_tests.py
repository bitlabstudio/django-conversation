"""Tests for the views of the ``conversation`` app."""
from django.core.urlresolvers import reverse
from django.test import TestCase

from django_libs.tests.factories import UserFactory
from django_libs.tests.views_tests import ViewTestMixin

from .factories import ConversationFactory


class ConversationRedirectViewTestCase(ViewTestMixin, TestCase):
    """Test case for the ConversationRedirectView view."""
    def setUp(self):
        self.user = UserFactory()

    def get_view_name(self):
        return 'conversation_list'

    def test_view(self):
        self.is_not_callable()
        self.is_callable(user=self.user,
                         and_redirects_to=reverse('conversation_create'))
        conversation = ConversationFactory()
        conversation.users.add(self.user)
        self.is_callable(and_redirects_to=reverse(
            'conversation_update', kwargs={'pk': conversation.pk}))


class ConversationCreateViewTestCase(ViewTestMixin, TestCase):
    """Test case for the ConversationCreateView view."""
    def setUp(self):
        self.user = UserFactory()
        self.stranger = UserFactory()

    def get_view_name(self):
        return 'conversation_create'

    def test_view(self):
        self.is_not_callable()
        self.is_callable(user=self.user)
        with self.settings(
                CONVERSATION_MESSAGE_FORM='conversation.forms.MessageForm'):
            self.is_callable(user=self.user)


class ConversationStartCreateViewTestCase(ViewTestMixin, TestCase):
    """
    Test case for the ConversationCreateView view, if direct messaging a user.

    """
    def setUp(self):
        self.user = UserFactory()
        self.stranger = UserFactory()

    def get_view_name(self):
        return 'conversation_start'

    def get_view_kwargs(self):
        return {'user_pk': self.stranger.pk}

    def test_view(self):
        self.is_not_callable()
        self.is_callable(user=self.user)
        self.is_callable(user=self.user, kwargs={'user_pk': 999})


class ConversationUpdateViewTestCase(ViewTestMixin, TestCase):
    """Test case for the ConversationUpdateView view."""
    def setUp(self):
        self.user = UserFactory()
        self.conversation = ConversationFactory()
        self.conversation.users.add(self.user)
        self.stranger = UserFactory()

    def get_view_name(self):
        return 'conversation_update'

    def get_view_kwargs(self):
        return {'pk': self.conversation.pk}

    def test_view(self):
        self.is_not_callable()
        self.is_not_callable(user=self.stranger)
        self.is_callable(user=self.user)
        self.is_callable(data={'text': 'Foobar'}, method='post')


class ConversationArchiveViewTestCase(ViewTestMixin, TestCase):
    """Test case for the ConversationArchiveView view."""
    def setUp(self):
        self.user = UserFactory()
        self.conversation = ConversationFactory()
        self.conversation.users.add(self.user)
        self.other_conversation = ConversationFactory()

    def get_view_name(self):
        return 'conversation_archive'

    def get_view_kwargs(self):
        return {'pk': self.conversation.pk}

    def test_view(self):
        self.is_not_callable()
        self.is_not_callable(user=self.user)
        self.is_not_callable(kwargs={'pk': self.other_conversation.pk},
                             method='post', ajax=True)
        self.is_callable(method='post', ajax=True)
        self.assertIn(
            self.user, self.conversation.archived_by.all(),
            msg=('The conversation should have been marked as archived.'))
