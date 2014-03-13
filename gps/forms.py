from django import forms
from django.forms import ModelForm
from gps.models import Session

class TestForm(forms.Form):
	content=forms.CharField(max_length=20)
	file =forms.FileField()

class SessionForm(ModelForm):
	class Meta:
		model = Session
		#fields = ['__all__']

from registration.forms import RegistrationForm
 
class ExRegistrationForm(RegistrationForm):
    gpstc_sailor_id = forms.DecimalField(label = "What is your GPSTC Sailor ID?:",min_value=0, max_value=9999)

