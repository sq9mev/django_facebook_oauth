from django.conf import settings
from django.utils.importlib import import_module
from fbgraph import GraphAPI, GraphAPIError



def _get_backend(backend=None):
    path=backend or getattr(settings, 'FB_BACKEND', 'facebook.fbbackends.FBConsoleBackend')
    try:
        mod_name, klass_name = path.rsplit('.', 1)
        mod = import_module(mod_name)
    except ImportError, e:
        raise ImproperlyConfigured(('Error importing FB backend module %s: "%s"'
                                    % (mod_name, e)))
    try:
        klass = getattr(mod, klass_name)
    except AttributeError:
        raise ImproperlyConfigured(('Module "%s" does not define a '
                                    '"%s" class' % (mod_name, klass_name)))
    return klass()

def fb_extend_access_token(access_token):
    graph=GraphAPI()
    new_token=graph.extend_access_token(access_token, 
        settings.FACEBOOK_APP_ID, settings.FACEBOOK_APP_SECRET)
    return new_token
    

def fb_post_as_app(profile_id, message, attachment=None, backend=None):
    backend=_get_backend(backend)
    backend.post_as_app(profile_id, message, attachment)

def fb_post_pages(message, attachment=None, backend=None):
    backend=_get_backend(backend)
    backend.post_pages(message, attachment)

def fb_put_like(access_token, what_to_like, backend=None):
    backend=_get_backend(backend)
    backend.put_like(access_token, what_to_like)
