from django.db import models


class FacebookProfile(models.Model):
    user = models.OneToOneField('auth.User')
    facebook_id = models.BigIntegerField()
    access_token = models.CharField(max_length=150, null=True, blank=True)

