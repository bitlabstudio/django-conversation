# flake8: noqa
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('conversation', '0004_auto_20151006_1512'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='conversation',
            name='read_by',
        ),
        migrations.AddField(
            model_name='conversation',
            name='read_by_all',
            field=models.DateTimeField(null=True, verbose_name='Read by all', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='conversation',
            name='unread_by',
            field=models.ManyToManyField(related_name='unread_conversations', null=True, verbose_name='Unread by', to=settings.AUTH_USER_MODEL, blank=True),
            preserve_default=True,
        ),
    ]
