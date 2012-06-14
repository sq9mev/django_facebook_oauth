from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.utils.translation import ugettext_lazy as _


class CreateUserForm(UserCreationForm):
    """form used to create new auth.models.User, must return User instance"""

    class Meta:
        model = User
        fields = ('username', 'email')

class ConnectUserForm(forms.Form):
    """form used to connect existing auth.models.User with FacebookProfile"""
    accept=forms.BooleanField(label=_('I Accept to connect my account in this service with my Facebook Account.'), required=True)

    def save(self, *args, **kwargs):
        pass


