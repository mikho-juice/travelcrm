# -*-coding: utf-8-*-

import logging

from pyramid.view import view_config, view_defaults
from pyramid.httpexceptions import HTTPFound

from . import BaseView
from ..models import DBSession
from ..models.crosspayment import Crosspayment
from ..lib.utils.common_utils import translate as _

from ..forms.crosspayments import (
    CrosspaymentForm, 
    CrosspaymentSearchForm,
    CrosspaymentAssignForm,
)


log = logging.getLogger(__name__)


@view_defaults(
    context='..resources.crosspayments.CrosspaymentsResource',
)
class CrosspaymentsView(BaseView):

    @view_config(
        request_method='GET',
        renderer='travelcrm:templates/crosspayments/index.mako',
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
        form = CrosspaymentSearchForm(self.request, self.context)
        form.validate()
        qb = form.submit()
        return {
            'total': qb.get_count(),
            'rows': qb.get_serialized()
        }

    @view_config(
        name='view',
        request_method='GET',
        renderer='travelcrm:templates/crosspayments/form.mako',
        permission='view'
    )
    def view(self):
        if self.request.params.get('rid'):
            resource_id = self.request.params.get('rid')
            crosspayment = Crosspayment.by_resource_id(resource_id)
            return HTTPFound(
                location=self.request.resource_url(
                    self.context, 'view', query={'id': crosspayment.id}
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
        renderer='travelcrm:templates/crosspayments/form.mako',
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
        form = CrosspaymentForm(self.request)
        if form.validate():
            crosspayment = form.submit()
            DBSession.add(crosspayment)
            DBSession.flush()
            return {
                'success_message': _(u'Saved'),
                'response': crosspayment.id
            }
        else:
            return {
                'error_message': _(u'Please, check errors'),
                'errors': form.errors
            }

    @view_config(
        name='edit',
        request_method='GET',
        renderer='travelcrm:templates/crosspayments/form.mako',
        permission='edit'
    )
    def edit(self):
        crosspayment = Crosspayment.get(self.request.params.get('id'))
        return {
            'item': crosspayment, 
            'title': self._get_title(_(u'Edit')),
        }

    @view_config(
        name='edit',
        request_method='POST',
        renderer='json',
        permission='edit'
    )
    def _edit(self):
        crosspayment = Crosspayment.get(self.request.params.get('id'))
        form = CrosspaymentForm(self.request)
        if form.validate():
            form.submit(crosspayment)
            return {
                'success_message': _(u'Saved'),
                'response': crosspayment.id
            }
        else:
            return {
                'error_message': _(u'Please, check errors'),
                'errors': form.errors
            }

    @view_config(
        name='copy',
        request_method='GET',
        renderer='travelcrm:templates/crosspayments/form.mako',
        permission='add'
    )
    def copy(self):
        crosspayment = Crosspayment.get(self.request.params.get('id'))
        return {
            'item': crosspayment,
            'title': self._get_title(_(u'Copy')),
        }

    @view_config(
        name='copy',
        request_method='POST',
        renderer='json',
        permission='add'
    )
    def _copy(self):
        return self._add()

    @view_config(
        name='details',
        request_method='GET',
        renderer='travelcrm:templates/crosspayments/details.mako',
        permission='view'
    )
    def details(self):
        crosspayment = Crosspayment.get(self.request.params.get('id'))
        return {
            'item': crosspayment,
        }

    @view_config(
        name='delete',
        request_method='GET',
        renderer='travelcrm:templates/crosspayments/delete.mako',
        permission='delete'
    )
    def delete(self):
        return {
            'title': self._get_title(_(u'Delete')),
            'rid': self.request.params.get('rid')
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
                items = DBSession.query(Crosspayment).filter(
                    Crosspayment.id.in_(ids)
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
        renderer='travelcrm:templates/crosspayments/assign.mako',
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
        form = CrosspaymentAssignForm(self.request)
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
