# -*-coding: utf-8-*-

import logging
import colander

from pyramid.view import view_config, view_defaults
from pyramid.httpexceptions import HTTPFound

from ..models import DBSession
from ..models.subaccount import Subaccount
from ..lib.utils.common_utils import translate as _
from ..lib.bl.subaccounts import get_bound_resource_by_subaccount_id
from ..forms.subaccounts import (
    SubaccountForm, 
    SubaccountSearchForm
)


log = logging.getLogger(__name__)


@view_defaults(
    context='..resources.subaccounts.SubaccountsResource',
)
class SubaccountsView(object):

    def __init__(self, context, request):
        self.context = context
        self.request = request

    @view_config(
        request_method='GET',
        renderer='travelcrm:templates/subaccounts/index.mako',
        permission='view'
    )
    def index(self):
        return {}

    @view_config(
        name='list',
        xhr='True',
        request_method='POST',
        renderer='json',
        permission='view'
    )
    def list(self):
        form = SubaccountSearchForm(self.request, self.context)
        form.validate()
        qb = form.submit()
        return {
            'total': qb.get_count(),
            'rows': qb.get_serialized()
        }

    @view_config(
        name='view',
        request_method='GET',
        renderer='travelcrm:templates/subaccounts/form.mako',
        permission='view'
    )
    def view(self):
        if self.request.params.get('rid'):
            resource_id = self.request.params.get('rid')
            subaccount = Subaccount.by_resource_id(resource_id)
            return HTTPFound(
                location=self.request.resource_url(
                    self.context, 'view', query={'id': subaccount.id}
                )
            )
        result = self.edit()
        result.update({
            'title': _(u"View Subaccount"),
            'readonly': True,
        })
        return result

    @view_config(
        name='add',
        request_method='GET',
        renderer='travelcrm:templates/subaccounts/form.mako',
        permission='add'
    )
    def add(self):
        return {'title': _(u'Add Subaccount')}

    @view_config(
        name='add',
        request_method='POST',
        renderer='json',
        permission='add'
    )
    def _add(self):
        form = SubaccountForm(self.request)
        if form.validate():
            subaccount, source = form.submit()
            DBSession.add(source)
            DBSession.flush()
            return {
                'success_message': _(u'Saved'),
                'response': subaccount.id
            }
        else:
            return {
                'error_message': _(u'Please, check errors'),
                'errors': form.errors
            }

    @view_config(
        name='edit',
        request_method='GET',
        renderer='travelcrm:templates/subaccounts/form.mako',
        permission='edit'
    )
    def edit(self):
        subaccount = Subaccount.get(self.request.params.get('id'))
        resource = get_bound_resource_by_subaccount_id(subaccount.id)
        return {
            'item': subaccount,
            'resource': resource,
            'title': _(u'Edit Subaccount'),
        }

    @view_config(
        name='edit',
        request_method='POST',
        renderer='json',
        permission='edit'
    )
    def _edit(self):
        subaccount = Subaccount.get(self.request.params.get('id'))
        form = SubaccountForm(self.request)
        if form.validate():
            form.submit(subaccount)
            return {
                'success_message': _(u'Saved'),
                'response': subaccount.id
            }
        else:
            return {
                'error_message': _(u'Please, check errors'),
                'errors': form.errors
            }

    @view_config(
        name='details',
        request_method='GET',
        renderer='travelcrm:templates/subaccounts/details.mako',
        permission='view'
    )
    def details(self):
        subaccount = Subaccount.get(self.request.params.get('id'))
        return {
            'item': subaccount,
        }


    @view_config(
        name='delete',
        request_method='GET',
        renderer='travelcrm:templates/subaccounts/delete.mako',
        permission='delete'
    )
    def delete(self):
        return {
            'title': _(u'Delete Subaccounts'),
            'rid': self.request.params.get('rid')
        }

    @view_config(
        name='delete',
        request_method='POST',
        renderer='json',
        permission='delete'
    )
    def _delete(self):
        errors = 0
        for id in self.request.params.getall('id'):
            item = Subaccount.get(id)
            if item:
                DBSession.begin_nested()
                try:
                    DBSession.delete(item)
                    DBSession.commit()
                except:
                    errors += 1
                    DBSession.rollback()
        if errors > 0:
            return {
                'error_message': _(
                    u'Some objects could not be delete'
                ),
            }
        return {'success_message': _(u'Deleted')}