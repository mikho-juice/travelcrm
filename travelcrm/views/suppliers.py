# -*-coding: utf-8-*-

import logging

from pyramid.view import view_config, view_defaults
from pyramid.response import Response
from pyramid.httpexceptions import HTTPFound

from . import BaseView
from ..models import DBSession
from ..models.resource import Resource
from ..models.supplier import Supplier
from ..lib.utils.common_utils import translate as _
from ..lib.helpers.fields import suppliers_combogrid_field
from ..forms.suppliers import (
    SupplierForm, 
    SupplierSearchForm,
    SupplierAssignForm,
)


log = logging.getLogger(__name__)


@view_defaults(
    context='..resources.suppliers.SuppliersResource',
)
class SuppliersView(BaseView):

    @view_config(
        request_method='GET',
        renderer='travelcrm:templates/suppliers/index.mako',
        permission='view'
    )
    def index(self):
        return {
            'title': self._get_title(),
        }

    @view_config(
        name='list',
        xhr='True',
        request_method='POST',
        renderer='json',
        permission='view'
    )
    def list(self):
        form = SupplierSearchForm(self.request, self.context)
        form.validate()
        qb = form.submit()
        return {
            'total': qb.get_count(),
            'rows': qb.get_serialized()
        }

    @view_config(
        name='view',
        request_method='GET',
        renderer='travelcrm:templates/suppliers/form.mako',
        permission='view'
    )
    def view(self):
        if self.request.params.get('rid'):
            resource_id = self.request.params.get('rid')
            supplier = Supplier.by_resource_id(resource_id)
            return HTTPFound(
                location=self.request.resource_url(
                    self.context, 'view', query={'id': supplier.id}
                )
            )
        result = self.edit()
        result.update({
            'title': self._get_title(_(u'View')),
            'readonly': True,
        })
        return result

    @view_config(
        name='add',
        request_method='GET',
        renderer='travelcrm:templates/suppliers/form.mako',
        permission='add'
    )
    def add(self):
        return {
            'title': self._get_title(_(u'Add')),
        }

    @view_config(
        name='add',
        request_method='POST',
        renderer='json',
        permission='add'
    )
    def _add(self):
        form = SupplierForm(self.request)
        if form.validate():
            supplier = form.submit()
            DBSession.add(supplier)
            DBSession.flush()
            return {
                'success_message': _(u'Saved'),
                'response': supplier.id
            }
        else:
            return {
                'error_message': _(u'Please, check errors'),
                'errors': form.errors
            }

    @view_config(
        name='edit',
        request_method='GET',
        renderer='travelcrm:templates/suppliers/form.mako',
        permission='edit'
    )
    def edit(self):
        supplier = Supplier.get(self.request.params.get('id'))
        return {
            'item': supplier,
            'title': self._get_title(_(u'Edit')),
        }

    @view_config(
        name='edit',
        request_method='POST',
        renderer='json',
        permission='edit'
    )
    def _edit(self):
        supplier = Supplier.get(self.request.params.get('id'))
        form = SupplierForm(self.request)
        if form.validate():
            form.submit(supplier)
            return {
                'success_message': _(u'Saved'),
                'response': supplier.id,
            }
        else:
            return {
                'error_message': _(u'Please, check errors'),
                'errors': form.errors
            }

    @view_config(
        name='details',
        request_method='GET',
        renderer='travelcrm:templates/suppliers/details.mako',
        permission='view'
    )
    def details(self):
        supplier = Supplier.get(self.request.params.get('id'))
        return {
            'item': supplier,
        }

    @view_config(
        name='delete',
        request_method='GET',
        renderer='travelcrm:templates/suppliers/delete.mako',
        permission='delete'
    )
    def delete(self):
        return {
            'title': self._get_title(_(u'Delete')),
            'id': self.request.params.get('id')
        }

    @view_config(
        name='delete',
        request_method='POST',
        renderer='json',
        permission='delete'
    )
    def _delete(self):
        errors = False
        ids = self.request.params.getall('id')
        if ids:
            try:
                items = DBSession.query(Supplier).filter(
                    Supplier.id.in_(ids)
                )
                for item in items:
                    DBSession.delete(item)
                DBSession.flush()
            except:
                errors=True
                DBSession.rollback()
        if errors:
            return {
                'error_message': _(
                    u'Some objects could not be delete'
                ),
            }
        return {'success_message': _(u'Deleted')}

    @view_config(
        name='assign',
        request_method='GET',
        renderer='travelcrm:templates/suppliers/assign.mako',
        permission='assign'
    )
    def assign(self):
        return {
            'id': self.request.params.get('id'),
            'title': self._get_title(_(u'Assign Maintainer')),
        }

    @view_config(
        name='assign',
        request_method='POST',
        renderer='json',
        permission='assign'
    )
    def _assign(self):
        form = SupplierAssignForm(self.request)
        if form.validate():
            form.submit(self.request.params.getall('id'))
            return {
                'success_message': _(u'Assigned'),
            }
        else:
            return {
                'error_message': _(u'Please, check errors'),
                'errors': form.errors
            }

    @view_config(
        name='combobox',
        request_method='POST',
        permission='view'
    )
    def _combobox(self):
        value = None
        resource = Resource.get(self.request.params.get('resource_id'))
        if resource:
            value = resource.supplier.id
        return Response(
            suppliers_combogrid_field(
                self.request, self.request.params.get('name'), value
            )
        )
