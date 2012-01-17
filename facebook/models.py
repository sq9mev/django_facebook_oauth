import json, urllib

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

class FacebookProfile(models.Model):
    user = models.OneToOneField(User)
    facebook_id = models.BigIntegerField(_('facebook uid'), blank=True, null=True)
    access_token = models.CharField(_('facebook access token'), blank=True, null=True, max_length=150)

    def get_facebook_profile(self):
        fb_profile = urllib.urlopen('https://graph.facebook.com/me?access_token=%s' % self.access_token)
        return json.load(fb_profile)
