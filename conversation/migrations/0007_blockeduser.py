# flake8: noqa
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('conversation', '0006_auto_20151007_0530'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlockedUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='Date')),
                ('blocked_by', models.ForeignKey(related_name='blocked_users', verbose_name='Blocked by', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(related_name='blocked', verbose_name='Blocked user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-date',),
                'verbose_name': 'Blocked user',
                'verbose_name_plural': 'Blocked users',
            },
            bases=(models.Model,),
        ),
    ]
