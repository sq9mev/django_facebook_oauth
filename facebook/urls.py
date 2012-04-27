from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('facebook.views',
    url(r'^auth/$', 'redirect_to_facebook_auth', name='facebook-auth'),
    url(r'^login/$', 'facebook_login', name='facebook-login'),
)
