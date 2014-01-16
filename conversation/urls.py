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
    url(r'^create/user/(?P<user_pk>\d+)/(?P<c_type>[-\w]+)/(?P<obj_id>\d+)/$',
        views.ConversationCreateView.as_view(),
        name='conversation_create_initial_content_object'),
    url(r'^create/user/(?P<user_pk>\d+)/$',
        views.ConversationCreateView.as_view(),
        name='conversation_create_initial'),
    url(r'^create/(?P<obj_id>\d+)/(?P<c_type>[-\w]+)/$',
        views.ConversationCreateView.as_view(),
        name='conversation_create_content_object'),
    url(r'^create/$',
        views.ConversationCreateView.as_view(),
        name='conversation_create'),
    url(r'^',
        views.ConversationRedirectView.as_view(),
        name='conversation_list'),
)
