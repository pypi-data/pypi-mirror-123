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
Autocomplete Handler for Products
"""

from __future__ import unicode_literals, absolute_import

import sqlalchemy as sa
from sqlalchemy import orm

from rattail.autocomplete import Autocompleter
from rattail.db import model


class ProductAutocompleter(Autocompleter):
    """
    Autocompleter for Products
    """
    autocompleter_key = 'products'
    model_class = model.Product
    autocomplete_fieldname = 'description'

    def make_autocomplete_query(self, session, term, **kwargs):
        model = self.model
        query = session.query(model.Product)\
                       .outerjoin(model.Brand)\
                       .filter(sa.or_(
                           model.Brand.name.ilike('%{}%'.format(term)),
                           model.Product.description.ilike('%{}%'.format(term))))

        query = self.filter_autocomplete_query(session, query)

        query = query.order_by(model.Brand.name, 
                               model.Product.description)\
                     .options(orm.joinedload(model.Product.brand))
        return query

    def filter_autocomplete_query(self, session, query, **kwargs):
        # do not show "deleted" items by default
        query = query.filter(model.Product.deleted == False)
        return query

    def autocomplete_display(self, product):
        return product.full_description


class ProductAllAutocompleter(ProductAutocompleter):
    """
    Autocompleter for Products, which shows *all* results, including
    "deleted" items etc.
    """

    def filter_autocomplete_query(self, session, query, **kwargs):
        return query
