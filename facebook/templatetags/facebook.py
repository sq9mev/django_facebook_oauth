from django import template

from registration.templatetags import button

register = template.Library()

register.tag('facebook_button', button('facebook/facebook_button.html'))
