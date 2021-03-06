# -*-coding: utf-8 -*-

import colander

from . import(
    ResourceSchema, 
    BaseForm,
    BaseSearchForm,
)
from .common import (
    currency_validator,
    service_validator
)
from ..resources.commissions import CommissionsResource
from ..models.commission import Commission
from ..lib.qb.commissions import CommissionsQueryBuilder
from ..lib.utils.security_utils import get_auth_employee


class _CommissionSchema(ResourceSchema):
    service_id = colander.SchemaNode(
        colander.String(),
        validator=service_validator
    )
    percentage = colander.SchemaNode(
        colander.Decimal(),
        validator=colander.Range(min=0, max=100)
    )
    price = colander.SchemaNode(
        colander.Money(),
    )
    currency_id = colander.SchemaNode(
        colander.String(),
        validator=currency_validator,
    )
    descr = colander.SchemaNode(
        colander.String(),
        validator=colander.Length(max=255),
        missing=u''
    )


class CommissionForm(BaseForm):
    _schema = _CommissionSchema

    def submit(self, commission=None):
        if not commission:
            commission = Commission(
                resource=CommissionsResource.create_resource(
                    get_auth_employee(self.request)
                )
            )
        commission.service_id = self._controls.get('service_id')
        commission.percentage = self._controls.get('percentage')
        commission.price = self._controls.get('price')
        commission.currency_id = self._controls.get('currency_id')
        commission.descr = self._controls.get('descr')
        return commission


class CommissionSearchForm(BaseSearchForm):
    _qb = CommissionsQueryBuilder
