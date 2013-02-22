from django.conf import settings
from fbgraph import GraphAPI, GraphAPIError
from tasks import *
import logging

logger=logging.getLogger('facebook')

class BaseFBBackend(object):

    def __init__(self):
        self.fb_objects_ids=getattr(settings, 'FACEBOOK_OBJECTS_IDS')


class FBGraphBackend(BaseFBBackend):


    def put_like(self, access_token, what_to_like):
        if not self.fb_objects_ids:
            logger.debug('Not posting any FB pages - not configured')
            return
        graph=GraphAPI(access_token=access_token)
        try:
            graph.put_like(str(what_to_like))
        except GraphAPIError, e:
            logger.error('Problem putting like %s -> %s FB: %s' % 
                (access_token, what_to_like, e))

    def post_pages(self, message, attachment=None):
            '''
            https://developers.facebook.com/docs/howtos/login/login-as-page/
            '''

            if not self.fb_objects_ids:
                logger.debug('Not posting any FB pages - not configured')
                return
            attachment=attachment or {}
            for (fbobj_id, access_token) in self.fb_objects_ids:
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

    def put_like(self, access_token, what_to_like):
        put_like.delay(access_token, what_to_like)

    def post_pages(self, message, attachment=None):
        post_pages.delay(message, attachment)

    def post_as_app(self, profile_id, message, attachment=None):
        post_as_app.delay(profile_id, message, attachment)


class FBLogBackend(object):

    def put_like(self, access_token, what_to_like):
        logger.info(u'Put like: %s -> %s' % (access_token, what_to_like))

    def post_pages(self, message, attachment=None):
        logger.info( u'Message: %s\nAttachment: %s' %
                (message, attachment))

    def post_as_app(self, profile_id, message, attachment=None):
        logger.info(u'Profile: %s\nMessage: %s\nAttachment: %s' % 
                (profile_id, message, attachment))

