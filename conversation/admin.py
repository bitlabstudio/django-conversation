"""Admin registration for the ``conversation`` app."""
from django.contrib import admin

import models


class ConversationAdmin(admin.ModelAdmin):
    list_display = ('user_emails', )

    def user_emails(self, obj):
        return ', '.join([str(u.email) for u in obj.users.all()])
    user_emails.short_description = 'User emails'


class MessageAdmin(admin.ModelAdmin):
    list_display = ('user', 'date')


admin.site.register(models.Conversation, ConversationAdmin)
admin.site.register(models.Message, MessageAdmin)
