"""Tests for the views of the ``conversation`` app."""
from django.contrib.contenttypes.models import ContentType
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


class ConversationCreateViewInitialTestCase(ViewTestMixin, TestCase):
    """
    Test case for the ConversationCreateView view, if direct messaging a user.

    """
    def setUp(self):
        self.user = UserFactory()
        self.stranger = UserFactory()

    def get_view_name(self):
        return 'conversation_create_initial'

    def get_view_kwargs(self):
        return {'user_pk': self.stranger.pk}

    def test_view(self):
        self.is_not_callable()
        self.is_not_callable(user=self.user, kwargs={'user_pk': 999})
        self.is_callable()


class ConversationCreateViewContentObjectTestCase(ViewTestMixin, TestCase):
    """
    Test case for the ConversationCreateView view, if a content object is
    attached to the conversation.

    """
    def setUp(self):
        self.user = UserFactory()
        self.content_object = UserFactory()

    def get_view_name(self):
        return 'conversation_create_content_object'

    def get_view_kwargs(self):
        return {
            'c_type': ContentType.objects.get_for_model(self.content_object),
            'obj_id': self.content_object.pk,
        }

    def test_view(self):
        self.is_not_callable()
        new_kwargs = self.get_view_kwargs()
        new_kwargs.update({'obj_id': 999})
        self.is_not_callable(user=self.user, kwargs=new_kwargs)
        new_kwargs = self.get_view_kwargs()
        new_kwargs.update({'c_type': 'foobar'})
        self.is_not_callable(user=self.user, kwargs=new_kwargs)
        self.is_callable()


class ConversationCreateViewInitialContentObjectTestCase(ViewTestMixin,
                                                         TestCase):
    """
    Test case for the ConversationCreateView view, if a content object is
    attached to the conversation and if an initial user has been chosen.

    """
    def setUp(self):
        self.user = UserFactory()
        self.content_object = UserFactory()
        self.stranger = UserFactory()

    def get_view_name(self):
        return 'conversation_create_initial_content_object'

    def get_view_kwargs(self):
        return {
            'c_type': ContentType.objects.get_for_model(self.content_object),
            'obj_id': self.content_object.pk,
            'user_pk': self.stranger.pk,
        }

    def test_view(self):
        self.is_not_callable()
        self.is_callable(user=self.user)


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
