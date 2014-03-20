from django import forms
from django.forms import ModelForm
from gps.models import Session, Equipment, SessionEquipment


class ImportSessions(forms.Form):

	content=forms.CharField(max_length=20)
	

	#	file =forms.FileField()
	


#class SessionForm(ModelForm):

class SessionForm(forms.Form):
	Full_Name=forms.CharField(max_length=20)

	#class Meta:
	#	model = Session
	#	#fields = ['__all__']


##
## add extra fields to replacement registration form
##

from registration.forms import RegistrationForm
 
class ExRegistrationForm(RegistrationForm):
    gpstc_sailor_id = forms.DecimalField(label = "What is your GPSTC Sailor ID?:",min_value=0, max_value=999999)
    gpstc_team_id = forms.DecimalField(label = "What is your GPSTC Team ID?:",min_value=0, max_value=999999)
   



