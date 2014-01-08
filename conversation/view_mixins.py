"""View mixins for the ``conversation`` app views."""
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponse
from django.utils.decorators import method_decorator

from django_libs.loaders import load_member

from .forms import MessageForm
from .models import Conversation


class ConversationViewMixin(object):
    """Mixin for conversation related views."""
    model = Conversation

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.user = request.user
        if kwargs.get('user_pk'):
            try:
                self.initial_user = User.objects.get(pk=kwargs['user_pk'])
            except User.DoesNotExist:
                pass
        if kwargs.get('pk'):
            # If it's not a CreateView, check the permission
            self.kwargs = kwargs
            self.object = self.get_object()
            if not request.user in self.object.users.all():
                raise Http404
        return super(ConversationViewMixin, self).dispatch(
            request, *args, **kwargs)

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

    def get_context_data(self, **kwargs):
        context = super(ConversationViewMixin, self).get_context_data(**kwargs)
        if hasattr(self, 'initial_user'):
            context.update({'initial_user': self.initial_user})
        return context

    def get_success_url(self):
        return reverse('conversation_update', kwargs={'pk': self.object.pk})


class ConversationStatusViewMixin(object):
    """
    Mixin for conversation related views, which change the conversation's
    status.

    """
    model = Conversation

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if request.method == 'POST' and request.is_ajax():
            self.kwargs = kwargs
            self.object = self.get_object()
            if not request.user in self.object.users.all():
                raise Http404
            if self.action == 'archive':
                self.object.archived_by.add(request.user)
                return HttpResponse('archived')
        raise Http404
