import unittest

class IslayAuthTestCase(unittest.TestCase):
    pass

def ForbiddenApp(environ, start_response):
    headers = []
    headers.append(('WWW-Authenticate', 'Basic realm="WSGI"'))

    start_response(401, headers)
    return