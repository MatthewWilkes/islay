import webob

from islay.auth.auth import AuthFactory

from islay.auth.tests.base import IslayAuthTestCase
from islay.auth.tests.base import ForbiddenApp
from islay.auth.tests.base import UnauthorisedApp

class TestUnauthorised(IslayAuthTestCase):
    
    def setUp(self):
        e={'HTTP_HOST':'example', 'wsgi.url_scheme':'http'}
        self.request = webob.Request(e)
        self.unauthorised = UnauthorisedApp
        self.app = AuthFactory({})(self.unauthorised)
    
    def test_unwrapped_application_returns_401(self):
        response = self.request.get_response(self.unauthorised)
        self.assertEqual(response.status, '401 Unauthorized')
    
    def test_middleware_hides_401(self):
        response = self.request.get_response(self.unauthorised)
        self.failIf(response.status.startswith('40'), '40x status code')

class TestChallenger(IslayAuthTestCase):
    
    def setUp(self):
        e={'HTTP_HOST':'example', 'wsgi.url_scheme':'http'}
        self.request = webob.Request(e)
        self.unauthorised = UnauthorisedApp
        self.forbidden = ForbiddenApp
        self.app = AuthFactory({}, challenger='islay.auth.tests.base.StaticTextChallenger')(self.unauthorised)
    
    def test_challenger_is_invoked_on_401(self):
        response = self.request.get_response(self.unauthorised)
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.body, 'Who do you think you are?')
    
    def test_challenger_passes_403(self):
        response = self.request.get_response(self.forbidden)
        self.assertEqual(response.status, '403 Forbidden')
