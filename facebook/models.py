from django.db import models
from django.contrib.sites.models import Site
from django.contrib.sites.managers import CurrentSiteManager


class FacebookProfile(models.Model):
    user = models.OneToOneField('auth.User')
    facebook_id = models.BigIntegerField()
    access_token = models.CharField(max_length=150, null=True, blank=True)

    site = models.ForeignKey(Site)
    objects = models.Manager()
    on_site = CurrentSiteManager()


