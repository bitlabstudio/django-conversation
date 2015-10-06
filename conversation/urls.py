"""URLs for the ``conversation`` app."""
from django.conf.urls import patterns, url

from . import views


urlpatterns = patterns(
    '',
    url(r'^(?P<pk>\d+)/archive/$',
        views.ConversationArchiveView.as_view(),
        name='conversation_archive'),
    url(r'^(?P<pk>\d+)/$',
        views.ConversationUpdateView.as_view(),
        name='conversation_update'),
    url(r'^create/(?P<user_pk>\d+)/$',
        views.ConversationCreateView.as_view(),
        name='conversation_create'),
    url(r'^',
        views.ConversationListView.as_view(),
        name='conversation_list'),
)
