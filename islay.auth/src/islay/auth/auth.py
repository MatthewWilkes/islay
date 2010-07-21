from webob import Request, Response

def AuthFactory(global_config, **local_conf):
    return AuthMiddleware

class AuthMiddleware(object):
    """An endpoint"""
    
    def __init__(self, app):
        self.app = app
    
    def __call__(self, environ, start_response):
        request = Request(environ)
        #print "Serving http://%s%s" % (environ['HTTP_HOST'], environ['PATH_INFO'])
        response = request.get_response(self.app)
        return response(environ, start_response)