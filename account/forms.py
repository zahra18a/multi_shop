from django import forms
from django.core import validators
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import User


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""

    password1 = forms.CharField(label="گذر وازه", widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="تکرار گذر واژه", widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ["phone"]

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    disabled password hash display field.
    """

    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ["phone", "password", "is_active", "is_admin"]

def start_with_0(value):
    print(type(value))
    print('*'*50)
    if value[0]!='0':
        raise  forms.ValidationError('phone should start with 0')
    if value[1]=='0':
        raise forms.ValidationError('phone should not second char is 0')

class LoginForm(forms.Form):
    phone = forms.CharField(label='مبایل', widget=forms.TextInput(attrs={'class': 'form-control'}), validators=[start_with_0])
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if len(phone) != 11:
            raise ValidationError(
                'Invalid value: %(value)s is not 11 characters long',
                code='invalid_phone',
                params={'value': f'{phone}'},
            )

class RegisterForm(forms.Form):
    phone= forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), validators=[start_with_0, validators.MaxLengthValidator(11)])

class CheckOtpForm(forms.Form):
    code=forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}),validators=[validators.MaxLengthValidator(4)])