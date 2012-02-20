from django.dispatch import Signal


# sent when user logs in through Facebook
facebook_login = Signal(providing_args=['graph'])

# sent when connecting through Facebook
facebook_connect = Signal(providing_args=['fbprofile', 'graph'])

