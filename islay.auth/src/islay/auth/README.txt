islay.auth
==========

islay.auth is a very basic authentication middleware designed to work well
within the WSGI specification. As not everything that works well in theory
also works well in practise the interfaces it uses are a strict subset of
those used by repoze.who, so any plugin that works for islay.auth should work
seamlessly in repoze.who which provides more features that may be of practical
use.

islay.auth will not scribble on the environ, it will only use HTTP standards.
That means it works by faking HTTP basic auth rather than simply providing the
details requested of it. For convenience it also provides REMOTE_USER
in-keeping with the de facto standard in use by Apache.

There are three types of plugin available:

- IIdentifier takes a request and manipulates its credentials. As well as
  extracting the credentials dictionary it provides helper methods for
  returning the appropriate headers to users to cause them to log in or out.

- IAuthenticator verifies that the extracted credentials correspond to a real
  user.

- IChallenger plugins take over in the case of a 401 response from the
  underlying application.

