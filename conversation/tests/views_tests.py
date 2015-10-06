"""Tests for the views of the ``conversation`` app."""
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.test import TestCase

from django_libs.tests.views_tests import ViewRequestFactoryTestMixin
from mixer.backend.django import mixer

from .. import views


class ConversationRedirectViewTestCase(ViewRequestFactoryTestMixin, TestCase):
    """Test case for the ConversationRedirectView view."""
    view_class = views.ConversationRedirectView

    def setUp(self):
        self.user = mixer.blend('auth.User')

    def test_view(self):
        self.should_redirect_to_login_when_anonymous()
        self.redirects(user=self.user, to=reverse('conversation_create'))
        conversation = mixer.blend('conversation.Conversation')
        conversation.users.add(self.user)
        self.redirects(user=self.user, to_url_name='conversation_update')


class ConversationCreateViewTestCase(ViewRequestFactoryTestMixin, TestCase):
    """Test case for the ConversationCreateView view."""
    view_class = views.ConversationCreateView

    def setUp(self):
        self.user = mixer.blend('auth.User')
        self.stranger = mixer.blend('auth.User')

    def test_view(self):
        self.should_redirect_to_login_when_anonymous()
        self.is_callable(user=self.user)
        self.is_callable(user=self.user, ajax=True)
        with self.settings(
                CONVERSATION_MESSAGE_FORM='conversation.forms.MessageForm'):
            self.is_callable(user=self.user)


class ConversationCreateViewInitialTestCase(
        ViewRequestFactoryTestMixin, TestCase):
    """
    Test case for the ConversationCreateView view, if direct messaging a user.

    """
    view_class = views.ConversationCreateView

    def setUp(self):
        self.user = mixer.blend('auth.User')
        self.stranger = mixer.blend('auth.User')

    def get_view_kwargs(self):
        return {'user_pk': self.stranger.pk}

    def test_view(self):
        self.should_redirect_to_login_when_anonymous()
        self.is_not_callable(user=self.user, kwargs={'user_pk': 999})
        self.is_callable(user=self.user)
        self.is_callable(user=self.user, ajax=True)


class ConversationCreateViewContentObjectTestCase(
        ViewRequestFactoryTestMixin, TestCase):
    """
    Test case for the ConversationCreateView view, if a content object is
    attached to the conversation.

    """
    view_class = views.ConversationCreateView

    def setUp(self):
        self.user = mixer.blend('auth.User')
        self.content_object = mixer.blend('auth.User')

    def get_view_kwargs(self):
        return {
            'c_type': ContentType.objects.get_for_model(self.content_object),
            'obj_id': self.content_object.pk,
        }

    def test_view(self):
        self.should_redirect_to_login_when_anonymous()
        new_kwargs = self.get_view_kwargs()
        new_kwargs.update({'obj_id': 999})
        self.is_not_callable(user=self.user, kwargs=new_kwargs)
        new_kwargs = self.get_view_kwargs()
        new_kwargs.update({'c_type': 'foobar'})
        self.is_not_callable(user=self.user, kwargs=new_kwargs)
        self.is_callable(user=self.user)
        self.is_callable(user=self.user, ajax=True)


class ConversationCreateViewInitialContentObjectTestCase(
        ViewRequestFactoryTestMixin, TestCase):
    """
    Test case for the ConversationCreateView view, if a content object is
    attached to the conversation and if an initial user has been chosen.

    """
    view_class = views.ConversationCreateView

    def setUp(self):
        self.user = mixer.blend('auth.User')
        self.content_object = mixer.blend('auth.User')
        self.stranger = mixer.blend('auth.User')

    def get_view_kwargs(self):
        return {
            'c_type': ContentType.objects.get_for_model(self.content_object),
            'obj_id': self.content_object.pk,
            'user_pk': self.stranger.pk,
        }

    def test_view(self):
        self.should_redirect_to_login_when_anonymous()
        self.is_callable(user=self.user)
        self.is_callable(user=self.user, ajax=True)


class ConversationUpdateViewTestCase(ViewRequestFactoryTestMixin, TestCase):
    """Test case for the ConversationUpdateView view."""
    view_class = views.ConversationUpdateView

    def setUp(self):
        self.user = mixer.blend('auth.User')
        self.conversation = mixer.blend('conversation.Conversation')
        self.conversation.users.add(self.user)
        self.stranger = mixer.blend('auth.User')

    def get_view_kwargs(self):
        return {'pk': self.conversation.pk}

    def test_view(self):
        self.should_redirect_to_login_when_anonymous()
        self.is_not_callable(user=self.stranger)
        self.is_callable(user=self.user)
        self.is_postable(user=self.user, data={'text': 'Foobar'},
                         to_url_name='conversation_update')
        self.is_callable(user=self.user, ajax=True)


class ConversationArchiveViewTestCase(ViewRequestFactoryTestMixin, TestCase):
    """Test case for the ConversationArchiveView view."""
    view_class = views.ConversationArchiveView

    def setUp(self):
        self.user = mixer.blend('auth.User')
        self.conversation = mixer.blend('conversation.Conversation')
        self.conversation.users.add(self.user)
        self.other_conversation = mixer.blend('conversation.Conversation')

    def get_view_kwargs(self):
        return {'pk': self.conversation.pk}

    def test_view(self):
        self.should_redirect_to_login_when_anonymous()
        self.is_not_callable(user=self.user)
        self.is_not_callable(kwargs={'pk': self.other_conversation.pk},
                             user=self.user, ajax=True, post=True)
        self.is_postable(user=self.user, ajax=True)
        self.assertIn(
            self.user, self.conversation.archived_by.all(),
            msg=('The conversation should have been marked as archived.'))
