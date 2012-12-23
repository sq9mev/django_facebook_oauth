from django import template
from django.conf import settings
from django.core.urlresolvers import reverse

from . import button

register = template.Library()

register.tag('facebook_button', button('facebook/facebook_button.html'))


@register.inclusion_tag('facebook/basic.js', takes_context=True)
def facebook_js(context):
    channel_url=context['request'].build_absolute_uri(reverse('fb_channel_html'))
    return {
        'FACEBOOK_APP_ID': settings.FACEBOOK_APP_ID,
        'channel_url': channel_url,
    }

                
