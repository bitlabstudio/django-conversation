# flake8: noqa
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('conversation', '0003_auto_20151006_1119'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='message',
            options={'ordering': ('pk',), 'verbose_name': 'Message', 'verbose_name_plural': 'Messages'},
        ),
        migrations.RemoveField(
            model_name='conversation',
            name='content_type',
        ),
        migrations.RemoveField(
            model_name='conversation',
            name='object_id',
        ),
    ]
