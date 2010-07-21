import unittest

class IslayAuthTestCase(unittest.TestCase):
    pass

def ForbiddenApp(environ, start_response):
    start_response(403, [])
    return