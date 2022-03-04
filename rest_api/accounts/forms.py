from django import forms
from django.core.validators import RegexValidator
from django.contrib.auth.password_validation import validate_password

class UserSetPassword(forms.Form):
    code = forms.CharField(label='Enter Code', max_length=100)
    new_password = forms.CharField(label='New Password', max_length=30,
    required=True, widget=forms.PasswordInput(),validators=[
        validate_password
    ]) 