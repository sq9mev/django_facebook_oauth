from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.hashers import make_password
from django import forms
from django.utils.translation import ugettext_lazy as _


class CreateUserForm(UserCreationForm):
    """form used to create new auth.models.User, must return User instance"""

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')


class ConnectUserForm(forms.Form):
    """form used to connect existing auth.models.User with FacebookProfile"""
    accept=forms.BooleanField(label=_('I Accept to connect my account in this service with my Facebook Account.'), required=True)

    def save(self, *args, **kwargs):
        pass


class NoPasswordUserCreationForm(forms.Form):
    username = forms.RegexField(regex=r'^[\w-]+$',
                                max_length=30,
                                label=_("Username"),
                                error_messages={'invalid': _("This value must contain only letters, numbers and underscores.")})
    email = forms.EmailField(max_length=75, label=_("Email address"))
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)

    def clean_username(self):
        # Since User.username is unique, this check is redundant,
        # but it sets a nicer error message than the ORM. See #13147.
        username = self.cleaned_data["username"]
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(self.error_messages['duplicate_username'])

    def save(self):
        cd=self.cleaned_data
        user=User(
                username=cd['username'], email=cd['email'],
                first_name=cd['first_name'], last_name=cd['last_name']
                )
        user.set_unusable_password()
        user.save()
        return user






