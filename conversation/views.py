"""Views for the ``conversation`` app."""
from django.core.urlresolvers import reverse
from django.views.generic import (
    CreateView,
    DetailView,
    RedirectView,
    UpdateView,
)

from . import view_mixins


class ConversationUpdateView(view_mixins.ConversationViewMixin, UpdateView):
    """View to update a conversation."""
    def dispatch(self, request, *args, **kwargs):
        resp = super(ConversationUpdateView, self).dispatch(
            request, *args, **kwargs)
        if hasattr(self, 'object'):
            self.object.read_by.add(request.user)
        return resp


class ConversationCreateView(view_mixins.ConversationViewMixin, CreateView):
    """View to start a new conversation."""
    pass


class ConversationRedirectView(view_mixins.ConversationViewMixin,
                               RedirectView):
    """View to list all conversations of a user."""
    permanent = False

    def get_redirect_url(self, **kwargs):
        if self.user.conversations.all():
            return reverse('conversation_update', kwargs={
                'pk': self.user.conversations.all()[0].pk})
        return reverse('conversation_create')


class ConversationArchiveView(view_mixins.ConversationStatusViewMixin,
                              DetailView):
    """View to archive a conversation."""
    action = 'archive'
