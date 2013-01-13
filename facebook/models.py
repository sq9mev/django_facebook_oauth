from django.db import models
from django.contrib.sites.models import Site
from django.contrib.sites.managers import CurrentSiteManager
from utils import fb_post_as_app, fb_extend_access_token


class FacebookProfile(models.Model):
    user = models.OneToOneField('auth.User')
    facebook_id = models.BigIntegerField()
    access_token = models.CharField(max_length=150, null=True, blank=True)
    expires = models.DateTimeField()
    extended = models.BooleanField(default=False)

    site = models.ForeignKey(Site)
    objects = models.Manager()
    on_site = CurrentSiteManager()

    def __unicode__(self):
        return 'FacebookProfile for %s' % self.user.username

    def extend_access_token(self):
        new_token=fb_extend_access_token(self.access_token)
        if 'access_token' in new_token:
            self.access_token=new_token['access_token']
            self.expires=new_token['expires']
            self.extended=True
            return new_token

    def post_as_app(self, message, attachments=None):
        fb_post_as_app(self.facebook_id, message, attachments)

