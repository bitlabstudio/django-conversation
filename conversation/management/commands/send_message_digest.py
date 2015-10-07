"""Command to send snippets of unread messages."""
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import NoArgsCommand
from django.utils.timezone import now, timedelta

from django_libs.utils_email import send_email

from ...models import Conversation


class Command(NoArgsCommand):
    help = "Send message digests."

    def handle_noargs(self, **options):
        # Get unread conversations, which hasn't been read for one day
        unread_conversations = Conversation.objects.filter(
            unread_by__isnull=False,
            read_by_all__lt=now() - timedelta(days=1))
        users = get_user_model().objects.filter(
            pk__in=unread_conversations.values_list('pk')).distinct()
        for user in users:
            send_email(
                None,
                {
                    'user': user,
                    'conversations': unread_conversations.filter(
                        unread_by__in=[user]),
                },
                'conversation/email/message_digest_subject.html',
                'conversation/email/message_digest_body.html',
                settings.FROM_EMAIL,
                recipients=[user.email, ],
                priority='medium',
            )
        print('Sent {0} digest(s).'.format(users.count()))
