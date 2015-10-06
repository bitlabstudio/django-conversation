# flake8: noqa
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('conversation', '0002_message_attachment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='conversation',
            name='archived_by',
            field=models.ManyToManyField(related_name='archived_conversations', null=True, verbose_name='Archived by', to=settings.AUTH_USER_MODEL, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='conversation',
            name='read_by',
            field=models.ManyToManyField(related_name='read_conversations', null=True, verbose_name='Read by', to=settings.AUTH_USER_MODEL, blank=True),
            preserve_default=True,
        ),
    ]
