from django.conf import settings
from fbgraph import GraphAPI, GraphAPIError
import logging


def fb_post_pages(message, attachment=None):
        '''
        https://developers.facebook.com/docs/howtos/login/login-as-page/
        '''

        FACEBOOK_OBJECTS_IDS=getattr(settings, 'FACEBOOK_OBJECTS_IDS')
        if not FACEBOOK_OBJECTS_IDS:
            logging.debug('Not posting any FB pages - not configured')
            return
        for (fbobj_id, access_token) in FACEBOOK_OBJECTS_IDS:
            graph=GraphAPI(access_token=access_token)
            try:
                graph.put_wall_post(message, profile_id=str(fbobj_id), attachment=attachment)
            except GraphAPIError, e:
                logging.error('Problem posting FB: %s' % e)


def fb_post_as_app(profile_id, message, attachment=None):
    attachment=attachment or {}
    graph=GraphAPI()
    graph.fetch_app_access_token()
    try:
        graph.put_wall_post(message, profile_id=str(profile_id), attachment=attachment)
    except GraphAPIError, e:
        logging.error('Problem posting FB: %s' % e)

