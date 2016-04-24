"""URLs for the ``conversation`` app."""
from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^block/(?P<user_pk>\d+)/$',
        views.BlockTriggerView.as_view(),
        name='conversation_block_user'),
    url(r'^(?P<pk>\d+)/(?P<action>[-\w]+)/$',
        views.ConversationTriggerView.as_view(),
        name='conversation_trigger'),
    url(r'^(?P<pk>\d+)/$',
        views.ConversationUpdateView.as_view(),
        name='conversation_update'),
    url(r'^create/(?P<user_pk>\d+)/$',
        views.ConversationCreateView.as_view(),
        name='conversation_create'),
    url(r'^',
        views.ConversationListView.as_view(),
        name='conversation_list'),
]
