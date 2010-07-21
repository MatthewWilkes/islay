from webob import Request, Response

def importFromName(path):
    parts = path.split('.')
    outer = '.'.join(parts[:-1])
    args = outer, globals(), locals(), parts[-1]
    module = __import__(*args)
    return getattr(module, parts[-1])

def AuthFactory(global_config, **local_conf):
    
    challengers = []
    
    for path in local_conf.get('challenger', '').split(','):
        if path:
            challengers.append(importFromName(path))
    
    class AuthMiddleware(object):
        """An endpoint"""
    
        def __init__(self, app):
            self.app = app
            self.challengers = challengers
    
        def __call__(self, environ, start_response):
            request = Request(environ)
            response = request.get_response(self.app)

            if response.status == '401 Unauthorized':
                for challenger in self.challengers:
                    challenge = challenger().challenge(environ, 
                                                       response.status, 
                                                       response.headers, 
                                                       [])
                    if challenge is None:
                        continue
                    else:
                        return challenge(environ, start_response)
        
            return response(environ, start_response)
    
    return AuthMiddleware

AuthMiddleware = AuthFactory({}) # Generic version without config