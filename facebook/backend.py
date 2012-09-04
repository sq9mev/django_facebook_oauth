from facebook.models import FacebookProfile
from django.contrib.auth.models import User


class FacebookBackend:
    profile_class = FacebookProfile

    def authenticate(self, facebook_uid=None):
        profile_class = self.get_profile_class()
        if not facebook_uid:
            return None
        try:
            return profile_class.objects.get(facebook_id=facebook_uid, site = Site.objects.get_current()).user
        except profile_class.DoesNotExist:
            return None

    def get_user(self, user_id):
        """ Just returns the user of a given ID. """
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

    def get_profile_class(self):
        return self.profile_class


    supports_object_permissions = False
    supports_anonymous_user = True
