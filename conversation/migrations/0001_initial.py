# flake8: noqa
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Conversation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('object_id', models.PositiveIntegerField(null=True, blank=True)),
                ('archived_by', models.ManyToManyField(related_name='archived_conversations', verbose_name='Archived by', to=settings.AUTH_USER_MODEL)),
                ('content_type', models.ForeignKey(related_name='conversation_content_objects', blank=True, to='contenttypes.ContentType', null=True)),
                ('read_by', models.ManyToManyField(related_name='read_conversations', verbose_name='Read by', to=settings.AUTH_USER_MODEL)),
                ('users', models.ManyToManyField(related_name='conversations', verbose_name='Users', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-pk',),
                'verbose_name': 'Conversation',
                'verbose_name_plural': 'Conversations',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='Date')),
                ('text', models.TextField(max_length=2048, verbose_name='Text')),
                ('conversation', models.ForeignKey(related_name='messages', verbose_name='Conversation', to='conversation.Conversation')),
                ('user', models.ForeignKey(related_name='messages', verbose_name='User', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-date',),
                'verbose_name': 'Message',
                'verbose_name_plural': 'Messages',
            },
            bases=(models.Model,),
        ),
    ]
