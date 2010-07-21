from webob import Request, Response

def importFromName(path):
    parts = path.split('.')
    outer = '.'.join(parts[:-1])
    args = outer, globals(), locals(), parts[-1]
    module = __import__(*args)
    return getattr(module, parts[-1])

def AuthFactory(global_config, **local_conf):
    
    identifiers = []
    authenticators = []
    challengers = []
    
    for path in local_conf.get('identifier', '').split(','):
        if path:
            identifiers.append(importFromName(path))

    for path in local_conf.get('authenticator', '').split(','):
        if path:
            authenticators.append(importFromName(path))

    for path in local_conf.get('challenger', '').split(','):
        if path:
            challengers.append(importFromName(path))

    
    class AuthMiddleware(object):
        """An endpoint"""
    
        def __init__(self, app):
            self.app = app
            self.identifiers = identifiers
            self.authenticators = authenticators
            self.challengers = challengers            
    
        def __call__(self, environ, start_response):
            request = Request(environ)

            auth = None
            identifier = None

            for identifier in self.identifiers:
                identifier = identifier()
                credentials = identifier.identify(environ)
                if credentials is None:
                    continue
                else:
                    for authenticator in authenticators:
                        auth = authenticator().authenticate(environ, credentials)
                        if auth is None:
                            continue
                        else:
                            break
            
            if auth:
                request.environ['REMOTE_USER'] = auth
            elif 'REMOTE_USER' in request.environ:
                del request.environ['REMOTE_USER']
            
            response = request.get_response(self.app)

            if response.status == '401 Unauthorized':
                for challenger in self.challengers:
                    if identifier is not None:
                        forget_headers = identifier.forget(environ, credentials)
                    else:
                        forget_headers = []
                    challenge = challenger().challenge(environ, 
                                                       response.status, 
                                                       response.headers, 
                                                       forget_headers)
                    if challenge is None:
                        continue
                    else:
                        return challenge(environ, start_response)
            else:
                if identifier is not None:
                    response.headers.update(identifier.remember(environ, credentials))
                return response(environ, start_response)
    
    return AuthMiddleware

AuthMiddleware = AuthFactory({}) # Generic version without config