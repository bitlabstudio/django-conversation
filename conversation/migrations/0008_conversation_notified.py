# flake8: noqa
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('conversation', '0007_blockeduser'),
    ]

    operations = [
        migrations.AddField(
            model_name='conversation',
            name='notified',
            field=models.ManyToManyField(related_name='notified_conversations', null=True, verbose_name='Notified', to=settings.AUTH_USER_MODEL, blank=True),
            preserve_default=True,
        ),
    ]
