# -*- coding: utf-8 -*-
#
# This file is part of famulus
#
# Copyright (C) 2016 Eric Le Bihan <eric.le.bihan.dev@free.fr>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#

"""
   famulus.uri
   ```````````

   Classes and helper functions for manipulating Uniform Resource Identifiers.

   :copyright: (C) 2016 Eric Le Bihan <eric.le.bihan.dev@free.fr>
   :license: GPLv3+
"""

import re
import urllib
from gettext import gettext as _


class InvalidURIError(Exception):
    """Error raised when an invalid URI is used"""
    def __init__(self, message=_("Invalid URI")):
        Exception.__init__(self, message)


def validate_uri(uri):
    """Validate an URI.

    @param uri: URI to validate
    @type uri: strip

    @raise: InvalidURIError
    """
    if not re.match(r'^(?:[\w]+)://'
                    r'(?:.+(?::.+)?@)?'
                    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
                    r'/dev/tty(?:[A-Z0-9]+)|'
                    r'/COM(?:[0-9]+)|'
                    r'localhost|'
                    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
                    r'(?:/?|[/?]\S+)$',
                    uri,
                    re.IGNORECASE):
        raise InvalidURIError


def rebuild_uri(uri, config, excluded_schemes):
    """Build full URI using values from configuration.

    @param uri: the URI to rebuild
    @type uri: str

    @param config: configuration
    @type config: :class:`Configuration`

    @param excluded_schemes: list of schemes which do not need a rebuild
    @type excluded_schemes: list of str

    @returns: rebuilt URI
    @rtype: str

    This function rebuilds a URI by adding omitted parameters such as the
    username or the password from the configuration.
    """
    validate_uri(uri)
    crumbs = urllib.parse.urlsplit(uri)
    if crumbs.scheme not in excluded_schemes:
        fields = list(crumbs)
        username = crumbs.username or config.username
        password = crumbs.password or config.password
        if username:
            netloc = username
            if password:
                netloc += ':' + password
            netloc += '@'
            if crumbs.hostname:
                netloc += crumbs.hostname
            fields[1] = netloc
        return urllib.parse.urlunsplit(fields)
    else:
        return uri

# vim: ts=4 sw=4 sts=4 et ai
