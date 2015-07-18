# -*-coding: utf-8-*-

import logging

from pyramid.view import view_config, view_defaults
from pyramid.httpexceptions import HTTPFound

from ..models import DBSession
from ..models.lead_item import LeadItem
from ..lib.utils.common_utils import translate as _

from ..forms.leads_items import (
    LeadItemSearchForm, 
    LeadItemForm
)


log = logging.getLogger(__name__)


@view_defaults(
    context='..resources.leads_items.LeadsItemsResource',
)
class LeadsItemsView(object):

    def __init__(self, context, request):
        self.context = context
        self.request = request

    @view_config(
        request_method='GET',
        renderer='travelcrm:templates/leads_items/index.mako',
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
        form = LeadItemSearchForm(self.request, self.context)
        form.validate()
        qb = form.submit()
        return {
            'total': qb.get_count(),
            'rows': qb.get_serialized()
        }

    @view_config(
        name='view',
        request_method='GET',
        renderer='travelcrm:templates/leads_items/form.mako',
        permission='view'
    )
    def view(self):
        if self.request.params.get('rid'):
            resource_id = self.request.params.get('rid')
            lead_item = LeadItem.by_resource_id(resource_id)
            return HTTPFound(
                location=self.request.resource_url(
                    self.context, 'view', query={'id': lead_item.id}
                )
            )
        result = self.edit()
        result.update({
            'title': _(u"View Lead Item"),
            'readonly': True,
        })
        return result

    @view_config(
        name='add',
        request_method='GET',
        renderer='travelcrm:templates/leads_items/form.mako',
        permission='add'
    )
    def add(self):
        return {'title': _(u'Add Lead Item')}

    @view_config(
        name='add',
        request_method='POST',
        renderer='json',
        permission='add'
    )
    def _add(self):
        form = LeadItemForm(self.request)
        if form.validate():
            lead_item = form.submit()
            DBSession.add(lead_item)
            DBSession.flush()
            return {
                'success_message': _(u'Saved'),
                'response': lead_item.id
            }
        else:
            return {
                'error_message': _(u'Please, check errors'),
                'errors': form.errors
            }

    @view_config(
        name='edit',
        request_method='GET',
        renderer='travelcrm:templates/leads_items/form.mako',
        permission='edit'
    )
    def edit(self):
        lead_item = LeadItem.get(self.request.params.get('id'))
        return {'item': lead_item, 'title': _(u'Edit Lead Item')}

    @view_config(
        name='edit',
        request_method='POST',
        renderer='json',
        permission='edit'
    )
    def _edit(self):
        lead_item = LeadItem.get(self.request.params.get('id'))
        form = LeadItemForm(self.request)
        if form.validate():
            form.submit(lead_item)
            return {
                'success_message': _(u'Saved'),
                'response': lead_item.id
            }
        else:
            return {
                'error_message': _(u'Please, check errors'),
                'errors': form.errors
            }

    @view_config(
        name='copy',
        request_method='GET',
        renderer='travelcrm:templates/leads_items/form.mako',
        permission='add'
    )
    def copy(self):
        lead_item = LeadItem.get(self.request.params.get('id'))
        return {
            'item': lead_item,
            'title': _(u"Copy Lead Item")
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
        renderer='travelcrm:templates/leads_items/details.mako',
        permission='view'
    )
    def details(self):
        lead_item = LeadItem.get(self.request.params.get('id'))
        return {
            'item': lead_item,
        }

    @view_config(
        name='delete',
        request_method='GET',
        renderer='travelcrm:templates/leads_items/delete.mako',
        permission='delete'
    )
    def delete(self):
        return {
            'title': _(u'Delete Leads Items'),
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
            item = LeadItem.get(id)
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