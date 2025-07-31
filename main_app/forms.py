from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError

from .models import User
from django import forms


class SignUpForm(forms.ModelForm):
    name = forms.CharField(max_length=50, label='Name', required=True)
    email = forms.EmailField(max_length=50, required=True)
    chief = forms.IntegerField(widget=forms.HiddenInput(attrs={'id':'chief_id'}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('name', 'email', 'password1')

    def save(self, commit=True):
        data = self.cleaned_data
        if data['chief']:
            data['chief'] = User.objects.get(id=data['chief'])
        if data['password1'] != data['password2']:
            return
        return User.objects.create_user(data['name'], data['email'], data['password1'], data['chief'])


class SignInForm(forms.Form):
    email = forms.EmailField(label='E-mail')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)


class PasswordChangeForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'id': 'old_password'}), label='Old password')
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'id': 'new_password1'}), label='New password')
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'id': 'new_password2'}), label='Confirm new password')
