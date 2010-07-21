import webob

from islay.auth.auth import AuthFactory

from islay.auth.tests.base import IslayAuthTestCase
from islay.auth.tests.base import ForbiddenApp

class TestForbidden(IslayAuthTestCase):
    
    def setUp(self):
        e={'HTTP_HOST':'example', 'wsgi.url_scheme':'http'}
        self.request = webob.Request(e)
        self.forbidden = ForbiddenApp
        self.app = AuthFactory({})(self.forbidden)
    
    def test_unwrapped_application_returns_401(self):
        response = self.request.get_response(self.forbidden)
        self.assertEqual(response.status, '401 Unauthorized')
    
    def test_middleware_hides_401(self):
        response = self.request.get_response(self.forbidden)
        self.failIf(response.status.startswith('40'), '40x status code')