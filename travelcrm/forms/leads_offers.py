# -*-coding: utf-8 -*-

import colander

from . import (
    ResourceSchema,
    BaseForm,
    BaseSearchForm,
)
from .common import (
    currency_validator,
    supplier_validator,
    service_validator,
)
from ..resources.leads_offers import LeadsOffersResource
from ..models.lead_offer import LeadOffer
from ..lib.qb.leads_offers import LeadsOffersQueryBuilder
from ..lib.utils.security_utils import get_auth_employee


class _LeadOfferSchema(ResourceSchema):
    service_id = colander.SchemaNode(
        colander.String(),
        validator=service_validator
    )
    supplier_id = colander.SchemaNode(
        colander.String(),
        validator=supplier_validator,
    )
    currency_id = colander.SchemaNode(
        colander.String(),
        validator=currency_validator
    )
    price = colander.SchemaNode(
        colander.Money(),
    )
    status = colander.SchemaNode(
        colander.String(),
    )
    descr = colander.SchemaNode(
        colander.String(),
        validator=colander.Length(max=255),
    )


class LeadOfferForm(BaseForm):
    _schema = _LeadOfferSchema

    def submit(self, lead_offer=None):
        if not lead_offer:
            lead_offer = LeadOffer(
                resource=LeadsOffersResource.create_resource(
                    get_auth_employee(self.request)
                )
            )

        lead_offer.service_id = self._controls.get('service_id')
        lead_offer.currency_id = self._controls.get('currency_id')
        lead_offer.supplier_id = self._controls.get('supplier_id')
        lead_offer.price = self._controls.get('price')
        lead_offer.status = self._controls.get('status')
        lead_offer.descr = self._controls.get('descr')
        return lead_offer


class LeadOfferSearchForm(BaseSearchForm):
    _qb = LeadsOffersQueryBuilder
