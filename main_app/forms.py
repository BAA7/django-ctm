from email.policy import default

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError

from .models import User, Task, Qualification, Language
from django import forms

from datetime import date


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


class TaskCreationForm(forms.ModelForm):
    name = forms.CharField(max_length=50, label='Name')
    deadline = forms.DateField(label='Deadline', widget=forms.DateInput(attrs={'type': 'date'}), initial=date.today)
    report_required = forms.BooleanField(label='Report required', required=False)
    performer = forms.ModelChoiceField(queryset=User.objects.all(), widget=forms.HiddenInput(attrs={'id': 'performer_id'}))
    language_required = forms.ModelChoiceField(queryset=Language.objects.all(), widget=forms.HiddenInput(attrs={'id': 'lang_id'}))
    qualifications_required = forms.ModelMultipleChoiceField(queryset=Qualification.objects.all(),
                                                             widget=forms.SelectMultiple(attrs={'id': 'selected_qualifications'}))

    class Meta:
        model = Task
        fields = ['name', 'deadline', 'report_required', 'performer', 'language_required', 'qualifications_required']
