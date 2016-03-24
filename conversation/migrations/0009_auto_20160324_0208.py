# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('conversation', '0008_conversation_notified'),
    ]

    operations = [
        migrations.AlterField(
            model_name='conversation',
            name='archived_by',
            field=models.ManyToManyField(related_name='archived_conversations', verbose_name='Archived by', to=settings.AUTH_USER_MODEL, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='conversation',
            name='notified',
            field=models.ManyToManyField(related_name='notified_conversations', verbose_name='Notified', to=settings.AUTH_USER_MODEL, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='conversation',
            name='unread_by',
            field=models.ManyToManyField(related_name='unread_conversations', verbose_name='Unread by', to=settings.AUTH_USER_MODEL, blank=True),
            preserve_default=True,
        ),
    ]
