from django.shortcuts import redirect
from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.utils.translation import ugettext_lazy as _
from forms import CreateUserForm, ConnectUserForm, NoPasswordUserCreationForm
import facebook
from fbgraph import GraphAPIError
import urllib
import signals
from unidecode import unidecode


def direct_to_template(request, template, extra_context=None, mimetype=None, **kwargs):
    """
    Render a given template with any extra URL parameters in the context as
    ``{{ params }}``.
    """
    if extra_context is None: extra_context = {}
    dictionary = {'params': kwargs}
    for key, value in extra_context.items():
        if callable(value):
            dictionary[key] = value()
        else:
            dictionary[key] = value
    c = RequestContext(request, dictionary)
    t = loader.get_template(template)
    return HttpResponse(t.render(c), content_type=mimetype)

def redirect_to_facebook_auth(request):
    """ First step of process, redirects user to facebook, which redirects to authentication_callback. """

    args = {
        'client_id': settings.FACEBOOK_APP_ID,
        'scope': settings.FACEBOOK_SCOPE,
        'redirect_uri': request.build_absolute_uri(reverse('facebook-login')),
    }
    return redirect('https://www.facebook.com/dialog/oauth?' + urllib.urlencode(args))


def catch_connection_error(func, template_name='facebook/failed.html'):
    """
    wrapper for Facebook connection error 
    """
    def wrapped(request, *args, **kw):
        message = _('Unknown error')
        try:
            return func(request, *args, **kw)
        except IOError:
            message = _('Could not connect to Facebook')
        except GraphAPIError, e:
            message = unicode(e)
        ctx = {
            'message': message,
            }
        return render_to_response(template_name, RequestContext(request, ctx))
    return wrapped


@catch_connection_error
def facebook_login(request, template_name='facebook/login.html',
        connect_template_name='facebook/login.html',
        fail_template_name='facebook/failed.html',
        extra_context=None, form_class=NoPasswordUserCreationForm,
        connect_form_class=ConnectUserForm,
        success_url=settings.LOGIN_REDIRECT_URL):
    """
    Facebook callback view
    """

    fb = facebook.create_facebook_proxy(request,
            request.build_absolute_uri(reverse('facebook-login')))

    if not fb.authorized():
        ctx = extra_context or {}
        ctx.update({
            'message': _('We couldn\'t validate your Facebook credentials.'),
            })
        return render_to_response(fail_template_name, RequestContext(request, ctx))


    if request.user.is_authenticated():
        form_class = connect_form_class
        user = request.user
    else:
        user = None

    if request.method == 'POST':

        form = form_class(data=request.POST)
        if form.is_valid():
            maybe_new_user = form.save()
            user = user or maybe_new_user #;)
            fb.get_or_create_local_profile(user)
            user = authenticate(facebook_uid=fb.uid)
            fbprofile = fb.get_profile()
            if user:
                signals.facebook_connect.send(sender=facebook_login,
                        instance=user, fbprofile=fbprofile, graph=fb.graph)
                login(request, user)
            return redirect(success_url)
    else:

        # try to authenticate previously connected facebook user
        # using facebook User ID
        
        user = authenticate(facebook_uid=fb.uid)
        if user:
            # user authenticated
            signals.facebook_login.send(sender=facebook_login,
                    instance=user, graph=fb.graph)
            login(request, user)
            return redirect(success_url)

        fbprofile = fb.get_profile()
        initials=dict((k, v) for (k, v) in fbprofile.iteritems() if k in ('first_name', 'last_name', 'email'))
        potential_username=fbprofile.get('username')
        
        if not potential_username:
            try:
                potential_username=u'-'.join(fbprofile.get('name').split())
            except AttributeError, e:
                logger.error('Error guessing username from fbprofile: %s' % fbprofile)
                potential_username=u'fb_%s' % fbprofile['id']
        username=unidecode(potential_username.lower().replace('.', '-'))

        sufix=0
        try_username=username
        while True:
            try:
                user=User.objects.get(username=try_username)
            except User.DoesNotExist:
                username=try_username
                break
            else:
                sufix+=1
                try_username=username + '-' + str(sufix)

        initials.update({'username': username})
        form = form_class(initial=initials)

    ctx = {
            'form': form,
            }
    return render_to_response(template_name, RequestContext(request, ctx))


