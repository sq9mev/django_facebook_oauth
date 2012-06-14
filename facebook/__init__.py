import fbgraph
from django.contrib.sites.models import Site
from facebook.models import FacebookProfile


class Facebook(object):
    """
    Simple Facebook proxy
    """

    def __init__(self, uid=None, access_token=None, url=None,
            local_profile_class = FacebookProfile):
        """
        Args:
            uid (str): Facebook user identifier
            access_token (str): facebook access token 
        """
        self.uid = uid
        self.graph = fbgraph.GraphAPI(access_token, url=url)
        self._profile = None
        self.local_profile_class = local_profile_class

        if self.graph.access_token and not self.uid:
            self.uid = self.get_user_id()

    def get_profile(self):
        """
        Fetch authenticated user profile data
        """
        if not self._profile or not self._profile['id']==self.uid:
            self._profile = self.graph.get_object('me')
        return self._profile

    def get_user_id(self):
        return self.graph.get_object('me', fields='id').get('id')
            
    def fetch_access_token(self, *args, **kw):
        self.graph.fetch_access_token(*args, **kw)
        if not self.uid and self.graph.access_token:
            self.uid = self.get_user_id()

    def authorized(self):
        return bool(self.uid)

    @property
    def access_token(self):
        return self.graph.access_token

    @property
    def user_id(self):
        return self.get_user_id()

    def get_or_create_local_profile(self, user):
        return self.local_profile_class.on_site.get_or_create(user = user,
                facebook_id = self.user_id, access_token = self.access_token,
                site = Site.objects.get_current()
                )



def create_facebook_proxy(request, redirect_uri=''):
    """
    Common Facebook proxy factory. 
    Uses FB cookie or request method (by `code` argument).

    `FACEBOOK_APP_ID` and `FACEBOOK_SECRET_KEY` comes from settings.

    Args:
        request: Django Request instance
        redirect_uri: Facebook redirect URI (required for "request" method)

    Returns:
        Preconfigured Facebook proxy instance
    """

    from django.conf import settings
    facebook_url = getattr(settings, 'FACEBOOK_URL', None)

    # request method
    if 'code' in request.GET:
        if not redirect_uri:
            raise ValueError('Redirect URI is required')
        proxy = Facebook(url=facebook_url)
        proxy.fetch_access_token(
                code=request.GET['code'], 
                app_id=settings.FACEBOOK_APP_ID,
                app_secret=settings.FACEBOOK_APP_SECRET,
                redirect_uri=redirect_uri
            )
        return proxy

    # cookie method
    fb_user = fbgraph.get_user_from_cookie(request.COOKIES,
        settings.FACEBOOK_APP_ID, settings.FACEBOOK_APP_SECRET)

    if fb_user:
        return Facebook(fb_user['uid'], fb_user['access_token'],
                url=facebook_url)

    return Facebook(url=facebook_url)


