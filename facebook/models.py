from django.db import models


class AbstractFacebookProfile(models.Model):
    user = models.OneToOneField('auth.User')
    facebook_id = models.BigIntegerField()
    access_token = models.CharField(max_length=150, null=True, blank=True)

    class Meta:
        abstract = True


class FacebookProfile(AbstractFacebookProfile):
    pass


