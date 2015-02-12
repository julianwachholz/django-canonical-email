# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re
from dns import resolver

from .settings import QUERY_MX


# mappings of providers and canonical format functions
KNOWN_DOMAINS = {
    'gmail.com': format_google_email,
}
KNOWN_MX_DOMAINS = {
    'aspmx.l.google.com': format_google_email,
}


def get_canonical_email(email):
    """
    Check the email address' domain for a known provider and format
    it to their specific canonical rules.

    """
    domain = email.split('@')[-1].lower()
    check_domains = KNOWN_DOMAINS

    if QUERY_MX and domain not in check_domains.keys():
        domain = get_mx_record_domain(domain)
        check_domains = KNOWN_MX_DOMAINS

    if domain in check_domains.keys():
        return check_domains[domain](email)

    return email


def get_mx_record_domain(domain):
    """
    Return the primary MX record for the domain.

    """
    records = resolver.query(domain, 'MX')
    return str(records[0].exchange).upper()


def format_google_email(email):
    """
    GMail and Google Apps for Business addresses
    treat emails with these rules:

    - Periods "." are not honoured.
    - Anything after a "+" sign acts as an alias

    """
    split = email.split('@')
    username = '@'.join(split[:-1])
    domain = split[-1]

    username = username.replace('.', '')
    username = re.sub(r'\+.+$', '', username)

    return '@'.join(username, domain)
