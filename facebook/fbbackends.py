from django.conf import settings
from fbgraph import GraphAPI, GraphAPIError
from tasks import *
import logging

logger=logging.getLogger('facebook')

class FBGraphBackend(object):
    def post_pages(self, message, attachment=None):
            '''
            https://developers.facebook.com/docs/howtos/login/login-as-page/
            '''

            FACEBOOK_OBJECTS_IDS=getattr(settings, 'FACEBOOK_OBJECTS_IDS')
            if not FACEBOOK_OBJECTS_IDS:
                logger.debug('Not posting any FB pages - not configured')
                return
            attachment=attachment or {}
            for (fbobj_id, access_token) in FACEBOOK_OBJECTS_IDS:
                graph=GraphAPI(access_token=access_token)
                try:
                    graph.put_wall_post(message, profile_id=str(fbobj_id), attachment=attachment)
                except GraphAPIError, e:
                    logger.error('Problem posting FB: %s' % e)

    def post_as_app(self, profile_id, message, attachment=None):
        attachment=attachment or {}
        graph=GraphAPI()
        graph.fetch_app_access_token()
        try:
            graph.put_wall_post(message, profile_id=str(profile_id), attachment=attachment)
        except GraphAPIError, e:
            logger.error('Problem posting FB: %s' % e)


class AsyncFBGraphBackend(FBGraphBackend):

    def post_pages(self, message, attachment=None):
        post_pages.delay(message, attachment)

    def post_as_app(self, profile_id, message, attachment=None):
        post_as_app.delay(profile_id, message, attachment)


class FBLogBackend(object):

    def post_pages(self, message, attachment=None):
        logger.info( u'Message: %s\nAttachment: %s' %
                (message, attachment))

    def post_as_app(self, profile_id, message, attachment=None):
        logger.info(u'Profile: %s\nMessage: %s\nAttachment: %s' % 
                (profile_id, message, attachment))
