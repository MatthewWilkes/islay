from webob import Request, Response

def AuthFactory(global_config, **local_conf):
    return AuthMiddleware

class AuthMiddleware(object):
    """An endpoint"""
    
    def __init__(self, app):
        self.app = app
    
    def __call__(self, environ, start_response):
        request = Request(environ)
        response = request.get_response(self.app)

        if response.status == '401 Unauthorized':
            NotImplemented
        
        return response(environ, start_response)