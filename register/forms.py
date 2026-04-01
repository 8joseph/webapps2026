from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm

from register.models import PayAppUser


class RegisterPayAppUserForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = PayAppUser
        fields = ['username','first_name', 'last_name', 'email','currency']
