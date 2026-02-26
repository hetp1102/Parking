
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from .models import Slot

class SignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username','email','password']

class LoginForm(AuthenticationForm): pass

class BookingForm(forms.Form):
    slot = forms.ModelChoiceField(queryset=Slot.objects.all())

class ScanForm(forms.Form):
    code = forms.CharField(label="Scanned Code", required=False)
