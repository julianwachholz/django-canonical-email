# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings


# Request DNS MX records for a domain to determine email provider
QUERY_MX = getattr(settings, 'CANONICAL_EMAIL_QUERY_MX', True)
