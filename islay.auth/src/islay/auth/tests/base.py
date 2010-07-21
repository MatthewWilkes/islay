import unittest
from zope.interface import implements

from islay.auth.interfaces import IChallenger

class IslayAuthTestCase(unittest.TestCase):
    pass

# Applications that mimic certain aspects of the authorisation dance

def UnauthorisedApp(environ, start_response):
    headers = []
    headers.append(('WWW-Authenticate', 'Basic realm="WSGI"'))

    start_response(401, headers)
    return

def ForbiddenApp(environ, start_response):
    headers = []
    start_response(403, headers)
    return


# Fake plugins we can use to make life easy

class StaticTextChallenger(object):
    implements(IChallenger)
    
    def challenge(self, environ, status, app_headers, forget_headers):
        def ChallengeApp(environ, start_response):
            headers = [("Content-type", "text/plain"), ]
            start_response(200, headers)
            return ["Who do you think you are?", ]
        return ChallengeApp

# Constants

MINIMAL_REQUEST = {'HTTP_HOST':'example', 
                   'wsgi.url_scheme':'http',
                   'PATH_INFO':'/',
                   'REQUEST_METHOD':'GET'}