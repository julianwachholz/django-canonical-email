# -*- coding: utf-8 -*-
from __future__ import unicode_literals


from django.db.models import EmailField

from .providers import get_canonical_email


class CanonicalEmailField(EmailField):
    """
    A canonical email field that normalizes email addresses
    specifically for some mail providers.

    """
    def __init__(self, email_field=None, *args, **kwargs):
        kwargs.setdefault('unique', True)
        self.email_field = email_field or 'email'
        super(CanonicalEmailField, self).__init__(*args, **kwargs)

    def pre_save(self, instance, add):
        email = getattr(instance, self.email_field)
        return get_canonical_email(email)


try:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], [r'^canonical_email\.fields\.CanonicalEmailField'])
except ImportError:
    pass
