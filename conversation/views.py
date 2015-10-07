"""Views for the ``conversation`` app."""
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.utils.timezone import now
from django.views.generic import (
    CreateView,
    DetailView,
    TemplateView,
    UpdateView,
)

from django_libs.loaders import load_member
from django_libs.views_mixins import AjaxResponseMixin

from .forms import MessageForm
from .models import Conversation


class ConversationViewMixin(AjaxResponseMixin):
    """Mixin for conversation related views."""
    model = Conversation

    def get_form_class(self):
        if hasattr(settings, 'CONVERSATION_MESSAGE_FORM'):
            return load_member(settings.CONVERSATION_MESSAGE_FORM)
        return MessageForm

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(ConversationViewMixin, self).get_form_kwargs(
            *args, **kwargs)
        kwargs.update({
            'user': self.user,
            'conversation': self.object,
            'instance': None,
            'initial_user': self.initial_user if hasattr(
                self, 'initial_user') else None,
        })
        return kwargs

    def get_success_url(self):
        return reverse('conversation_update', kwargs={'pk': self.object.pk})


class ConversationUpdateView(ConversationViewMixin, UpdateView):
    """View to update a conversation."""
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.user = request.user
        # Check the permission
        self.kwargs = kwargs
        self.object = self.get_object()
        if self.user not in self.object.users.all():
            raise Http404
        # Mark as read
        self.object.unread_by.remove(self.user)
        # If conversation has been read by all participants
        if self.object.unread_by.count() == 0:
            self.object.read_by_all = now()
            self.object.save()
        return super(ConversationUpdateView, self).dispatch(
            request, *args, **kwargs)


class ConversationCreateView(ConversationViewMixin, CreateView):
    """View to start a new conversation."""
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.user = request.user
        try:
            self.initial_user = get_user_model().objects.get(
                pk=kwargs['user_pk'])
        except get_user_model().DoesNotExist:
            raise Http404
        # Check for an existing conversation of these users
        conversations = self.user.conversations.filter(
            pk__in=self.initial_user.conversations.values_list('pk'))
        if conversations:
            return HttpResponseRedirect(reverse(
                'conversation_update', kwargs={'pk': conversations[0]}))
        return super(ConversationCreateView, self).dispatch(
            request, *args, **kwargs)


class ConversationListView(TemplateView):
    """View to list all conversations of a user."""
    template_name = 'conversation/conversation_list.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        active_conversations = request.user.conversations.exclude(
            archived_by__in=[request.user])
        if active_conversations:
            return HttpResponseRedirect(reverse('conversation_update', kwargs={
                'pk': active_conversations[0].pk}))
        return super(ConversationListView, self).dispatch(
            request, *args, **kwargs)


class ConversationArchiveView(DetailView):
    """View to archive a conversation."""
    model = Conversation

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if request.method == 'POST':
            self.kwargs = kwargs
            self.object = self.get_object()
            if request.user not in self.object.users.all():
                raise Http404
            self.object.archived_by.add(request.user)
            return HttpResponseRedirect(reverse('conversation_list'))
        raise Http404
