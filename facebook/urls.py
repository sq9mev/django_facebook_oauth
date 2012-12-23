from django.conf.urls.defaults import patterns, url
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('facebook.views',
    url(r'^auth/$', 'redirect_to_facebook_auth', name='facebook-auth'),
    url(r'^login/$', 'facebook_login', name='facebook-login'),
    url(r'^channel.html$', direct_to_template, {'template': 'facebook/channel.html'}, name='fb_channel_html'),
)
