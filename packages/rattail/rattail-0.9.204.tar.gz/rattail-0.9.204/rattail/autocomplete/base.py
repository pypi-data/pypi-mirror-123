# -*- coding: utf-8 -*-
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
Autocomplete handlers - base class
"""

from __future__ import unicode_literals, absolute_import

import sqlalchemy as sa


class Autocompleter(object):
    """
    Base class and partial default implementation for autocomplete
    handlers.  It is expected that all autocomplete handlers will
    ultimately inherit from this base class, therefore it defines the
    implementation "interface" loosely speaking.  Custom autocomplete
    handlers are welcome to supplement or override this as needed, and
    in fact must do so for certain aspects.

    .. attribute: autocompleter_key
       The key indicates what "type" of autocompleter this is.  It
       should be a string, e.g. ``'products'``.  It will generally
       correspond to the route names used in Tailbone, though not
       always.  
    """
    autocompleter_key = None

    def __init__(self, config):
        if not self.autocompleter_key:
            raise NotImplementedError("You must define `autocompleter_key` "
                                      "attribute for handler class: {}".format(
                                          self.__class__))
        self.config = config
        self.app = self.config.get_app()
        self.enum = config.get_enum()
        self.model = config.get_model()

    def get_model_class(self):
        return self.model_class

    @property
    def autocomplete_fieldname(self):
        raise NotImplementedError("You must define `autocomplete_fieldname` "
                                  "attribute for handler class: {}".format(
                                      self.__class__))

    def autocomplete(self, session, term, **kwargs):
        """
        The main reason this class exists.  This method accepts a
        ``term`` (string) argument and will return a sequence of
        matching results.
        """
        term = self.prepare_autocomplete_term(term)
        if not term:
            return []

        results = self.get_autocomplete_data(session, term)
        return [{'label': self.autocomplete_display(x),
                 'value': self.autocomplete_value(x)}
                for x in results]

    def prepare_autocomplete_term(self, term, **kwargs):
        """
        If necessary, massage the incoming search term for use with
        the autocomplete query.
        """
        return term

    def get_autocomplete_data(self, session, term, **kwargs):
        """
        Collect data for all matching results, for the given search term.
        """
        query = self.make_autocomplete_query(session, term)
        return query.all()

    def make_autocomplete_query(self, session, term, **kwargs):
        """
        Build the complete query from which to obtain search results.
        """
        # we are querying one table (and column) primarily
        model_class = self.get_model_class()
        query = session.query(model_class)

        # filter according to business logic etc. if applicable
        query = self.filter_autocomplete_query(session, query)

        # filter according to search term(s)
        column = getattr(model_class, self.autocomplete_fieldname)
        criteria = [column.ilike('%{}%'.format(word))
                    for word in term.split()]
        query = query.filter(sa.and_(*criteria))

        # sort results by something meaningful
        query = query.order_by(column)
        return query

    def filter_autocomplete_query(self, session, query, **kwargs):
        return query

    def autocomplete_display(self, obj):
        return getattr(obj, self.autocomplete_fieldname)

    def autocomplete_value(self, obj):
        return obj.uuid
