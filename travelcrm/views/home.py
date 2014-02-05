# -*-coding: utf-8-*-

import colander
from pyramid.httpexceptions import (
    HTTPFound,
)
from pyramid.security import (
    remember,
    forget,
    authenticated_userid
)
from pyramid.view import view_config
from pyramid.view import forbidden_view_config

from ..resources import Root
from ..models import User

from ..forms.auth import (
    LoginSchema,
    ForgotSchema
)


class Home(object):

    def __init__(self, context, request):
        self.context = context
        self.request = request

    @view_config(
        request_method='GET',
        context='..resources.Root',
        renderer='travelcrm:templates/home.mak',
        permission='view'
    )
    def index(self):
        return {}

    @view_config(
        name='forgot',
        request_method='GET',
        context='..resources.Root',
        renderer='travelcrm:templates/auth/forgot.mak',
    )
    def forgot(self):
        auth_url = self.request.resource_url(
            Root(self.request),
            'auth'
        )
        return {'auth_url': auth_url}

    @view_config(
        name='forgot',
        request_method='POST',
        context='..resources.Root',
        renderer='json',
    )
    def _forgot(self):
        # TODO: complete this functionality
        _ = self.request.translate
        schema = ForgotSchema()
        try:
            schema.deserialize(self.request.params)
        except colander.Invalid, e:
            return {
                'error_message': _(u'Please, check errors'),
                'errors': e.asdict()
            }
        return {
            'success_message': _(u'Check your email'),
            'close': False
        }

    @forbidden_view_config(
        request_method="GET",
        renderer="travelcrm:templates/auth/login.mak",
    )
    @view_config(
        name='auth',
        request_method='GET',
        context='..resources.Root',
        renderer='travelcrm:templates/auth/login.mak',
    )
    def auth(self):
        if authenticated_userid(self.request):
            return HTTPFound(
                location=self.request.resource_url(self.context)
            )

        forgot_url = self.request.resource_url(
            Root(self.request),
            'forgot'
        )
        auth_url = self.request.resource_url(
            Root(self.request),
            'auth'
        )
        return {
            'forgot_url': forgot_url,
            'auth_url': auth_url
        }

    @view_config(
        name='auth',
        request_method='POST',
        context='..resources.Root',
        renderer='json',
    )
    def _auth(self):
        _ = self.request.translate
        schema = LoginSchema()

        controls = schema.deserialize(self.request.params)
        user = User.by_username(controls.get('username'))

        if (user
            and user.validate_password(controls.get('password'))
            and user.resource.is_active()
            and user.employee
        ):
            self.request.response.headers = remember(self.request, user.id)
            return {
                'redirect': self.request.resource_url(self.context),
                'success_message': _(u"Success, wait...")
            }
        return {
            'error_message': _(u'Invalid username or password'),
        }

    @view_config(
        name='logout',
        request_method='GET',
        context='..resources.Root',
        renderer='travelcrm:templates/auth/logout.mak'
    )
    def logout(self):
        return {}

    @view_config(
        name='logout',
        request_method='POST',
        context='..resources.Root'
    )
    def _logout(self):
        redirect_url = self.request.resource_url(Root(self.request))
        return HTTPFound(location=redirect_url, headers=forget(self.request))
