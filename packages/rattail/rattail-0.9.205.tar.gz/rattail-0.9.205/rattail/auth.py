# -*- coding: utf-8; -*-
################################################################################
#
#  Rattail -- Retail Software Framework
#  Copyright © 2010-2021 Lance Edgar
#
#  This file is part of Rattail.
#
#  Rattail is free software: you can redistribute it and/or modify it under the
#  terms of the GNU General Public License as published by the Free Software
#  Foundation, either version 3 of the License, or (at your option) any later
#  version.
#
#  Rattail is distributed in the hope that it will be useful, but WITHOUT ANY
#  WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
#  FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
#  details.
#
#  You should have received a copy of the GNU General Public License along with
#  Rattail.  If not, see <http://www.gnu.org/licenses/>.
#
################################################################################
"""
Auth Handler

See also :doc:`rattail-manual:base/handlers/other/auth`.
"""

from __future__ import unicode_literals, absolute_import

from rattail.app import GenericHandler


class AuthHandler(GenericHandler):
    """
    Base class and default implementation for auth handlers.
    """

    def authenticate_user(self, session, username, password):
        """
        Try to authenticate the given credentials.  If successful,
        this should return a Rattail ``User`` instance; otherwise
        returns ``None``.
        """
        from rattail.db.auth import authenticate_user

        return authenticate_user(session, username, password)

    def generate_unique_username(self, session, **kwargs):
        """
        Generate a unique username using data from ``kwargs`` as hints.
        """
        model = self.model

        original_username = self.generate_username(session, **kwargs)
        username = original_username

        # only if given a session, can we check for unique username
        if session:
            counter = 1
            while True:
                users = session.query(model.User)\
                               .filter(model.User.username == username)\
                               .count()
                if not users:
                    break
                username = "{}{:02d}".format(original_username, counter)
                counter += 1

        return username

    def generate_username(self, session, **kwargs):
        """
        Generate a unique username using data from ``kwargs`` as hints.
        """
        person = kwargs.get('person')
        if person:
            first = (person.first_name or '').strip().lower()
            last = (person.last_name or '').strip().lower()
            return '{}.{}'.format(first, last)
            
        return 'newuser'

    def make_user(self, **kwargs):
        """
        Make and return a new User instance.
        """
        model = self.model
        session = kwargs.pop('session', None)

        if 'username' not in kwargs:
            kwargs['username'] = self.generate_unique_username(session, **kwargs)

        user = model.User(**kwargs)
        return user
