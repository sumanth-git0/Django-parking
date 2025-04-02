from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from .models import parkuser,parkhistory, parkspace


class SignUpForm(UserCreationForm):

    class Meta:
        model = parkuser
        fields = ['username', 'email', 'password1', 'password2']


class add_book(forms.ModelForm):

    class Meta:
        model = parkhistory
        fields = ['Level','Type','VehicleNumber']
