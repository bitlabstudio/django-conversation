"""Template tags for the ``conversation`` app."""
from django.template import Library
from django.template.defaultfilters import truncatechars

register = Library()


@register.assignment_tag
def chain_user_names(users, exclude_user, truncate=35):
    """Tag to return a truncated chain of user names."""
    if not users:
        return ''
    return truncatechars(
        ', '.join(u'{}'.format(u) for u in users.exclude(pk=exclude_user.pk)),
        truncate)
