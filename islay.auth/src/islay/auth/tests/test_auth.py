import webob

from islay.auth.auth import AuthFactory

from islay.auth.tests.base import IslayAuthTestCase
from islay.auth.tests.base import OKApp
from islay.auth.tests.base import MINIMAL_REQUEST
import islay.auth.tests.base

class TestIdentifiers(IslayAuthTestCase):
    
    def setUp(self):
        environ = MINIMAL_REQUEST.copy()
        environ.update({'REMOTE_USER':'example'})
        self.request = webob.Request(environ)
        self.ok = OKApp
        self.app = AuthFactory({}, identifier='islay.auth.tests.base.GlobalNoteRemoteUser',)(self.ok)
        islay.auth.tests.base.creds = None

    def test_app_is_ok(self):
        response = self.request.get_response(self.app)
        self.assertEqual(response.status, '200 OK')
    
    def test_app_stores_creds(self):
        response = self.request.get_response(self.app)
        self.assertEqual(islay.auth.tests.base.creds, {'user':'example'})
    