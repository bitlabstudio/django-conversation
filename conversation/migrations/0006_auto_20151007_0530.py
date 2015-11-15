# flake8: noqa
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('conversation', '0005_auto_20151007_0430'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='message',
            options={'ordering': ('date',), 'verbose_name': 'Message', 'verbose_name_plural': 'Messages'},
        ),
        migrations.AlterField(
            model_name='conversation',
            name='read_by_all',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 7, 10, 30, 7, 553674, tzinfo=utc), verbose_name='Read by all', auto_now_add=True),
            preserve_default=False,
        ),
    ]
