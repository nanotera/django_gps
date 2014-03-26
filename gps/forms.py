from django import forms
from django.forms import ModelForm
from gps.models import Session, Equipment, SessionEquipment
from django.contrib.formtools.preview import FormPreview
from django.http import HttpResponseRedirect
from django.core.exceptions import ValidationError

import pdb

##
##
##
myglobal_message=''

class ProcessSessionsForm(forms.Form):

	def validate_userid(value):
		pdb.set_trace()
		my_message=''
		#if (value=='nomessage'):
		
		myglobal_message=my_message
		#raise ValidationError(' %s look at that output from validator.' % value )


	def validate_my_message(value):
		my_message=myglobal_message
		#return my_message


	my_user=forms.CharField(max_length=20 )
	my_message = forms.CharField(widget=forms.Textarea, initial='')
	my_yesno=forms.BooleanField(label='Tick this to process all the sessions')

	#my_user=forms.CharField(max_length=20, validators= [validate_userid] )
	#my_message = forms.CharField(widget=forms.Textarea, initial='')
	#my_yesno=forms.BooleanField(label='Tick this to process all the sessions', validators= [validate_my_message])
	

	def clean(self):
		pdb.set_trace()
		cleaned_data = super(ProcessSessionsForm, self).clean()
		userid=cleaned_data.get('my_user')
		print userid
		import pprint
		pprint.pprint(cleaned_data)
		my_message=''
        	for s in Session.objects.filter(user_id = userid ): 
			my_message=my_message + '\n' +  s.NickName
		
		
		print my_message    
		cleaned_data['my_message']=my_message
		#self.data['my_message']=my_message
        	 
		#raise forms.ValidationError("look at that output from form cleaned.")
		#self._errors['my_message']= self.error_class('error added')

        	return cleaned_data


##
##
##


class ImportSessions(forms.Form):

	content=forms.CharField(max_length=20)
	#	file =forms.FileField()
	
##
##
##



class GetSailorID(forms.Form):


	def getsailoridmymessage():
		import urllib2, StringIO, pdb, re, pprint 
		from gps.models import Location

		url="http://www.ka72.com/biglist.aspx"

		print url
		#pdb.set_trace()
		try: 
			webstream = urllib2.urlopen(url)
			data=webstream.read().decode('utf-8')
		except:
			print "oops an error occurred opening the url"
			data=""

		data=StringIO.StringIO(data)
		started=False
		ndata=[]
		ntext=''
		
		myregexp1=re.compile('^.*?="')
		myregexp2=re.compile('">.*$')
		for l in data:
			if started and 'value=' in l and  not 'selected' in l :
				newl=(myregexp2.sub('',myregexp1.sub('',l)).replace('\n',''))
				country=newl[-2:]
				#print country
				if country=='AU':
					newl1=newl.encode('ascii','ignore')
					ndata.append(newl1)
					ntext=ntext+ newl1 + '\n'
					nfields=map(str.strip,newl1.split(','))
					pprint.pprint(nfields)
					nf=len(nfields)
					nme=''
					ste=''


					# if too many items join them back together
					if nf > 3 :
						nme=nfields[0]
						for i in range(nf-3):
							nme=nme+','+nfields[i+1]
						ste=nfields[nf-2].upper()
					elif nf == 3 :
						nme=nfields[0]
						ste=nfields[1].upper()
					elif nf ==2  :
						nme=nfields[0]
						ste=nfields[0].upper()
					elif nf ==1  :
						nme=nfields[0]

										
					#pdb.set_trace()
					## ONLY ADD NEW ONES - NOT EDITING OLD ONES ANYMORE

					try:
						newlocation=Location.objects.get(Name=nme)

					except:
						newlocation=Location()
						newlocation.Country='AU'
						newlocation.Name=nme
						newlocation.State=ste
						newlocation.Description=newl1
						newlocation.KeyWords=nme
						newlocation.save()

			if 'list sorted by timezone' in l :
				#pdb.set_trace()
				started=True
			else:
				if started and '</select>' in l :
					started=False
					#pdb.set_trace()
		
		return ntext



	content=forms.CharField(max_length=20)
	gpstc_sailor_id = forms.DecimalField(label = "What is your GPSTC Sailor ID?:",min_value=0, max_value=999999)
	gpstc_team_id = forms.DecimalField(label = "What is your GPSTC Team ID?:",min_value=0, max_value=999999)
	#my_message = forms.CharField(widget=forms.Textarea, default=getsailoridmymessage())

	my_message = forms.CharField(widget=forms.Textarea, initial=getsailoridmymessage)


##
##
##



class GetSailorIDFormPreview(FormPreview):

	def done(self, request, cleaned_data):
		#pdb.set_trace()
		return HttpResponseRedirect('/')
	

##
##
##

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
    FullName = forms.CharField(label = "What is your GPSTC FullName?:")
    NickName = forms.CharField(label = "What is your GPSTC NickName?:")
   



