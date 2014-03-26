# Create your views here.
#from django.forms import ModelForm
from django.shortcuts import render
from django.template import Context, loader
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse

from django.contrib.auth.decorators import login_required

from gps.forms import SessionForm, ImportSessions, GetSailorID, ProcessSessionsForm
from gps.models import UserProfile
from gps.models import Session, Equipment, Location, SessionEquipment

import csv,  urllib2, StringIO, re, sys

from datetime import datetime

from django.utils import timezone

import pdb


##
##
##

from django_tables2   import RequestConfig
from gps.tables  import SessionTable

@login_required
def SessionsAsTable(request):
    #import pdb
    #pdb.set_trace()
    table = SessionTable(Session.objects.filter(user_id = request.user.id ).values('FullName','SessionDate','Two_Second_Peak','Five_X_10_Second_Average','Alpha_Racing_500m','Nautical_Mile','One_Hour'))
    RequestConfig(request).configure(table)
    return render(request, 'gps/session_list.html', {'table': table})

##
##
##

@login_required
def sessionform(request, pk):
	import pdb
	pdb.set_trace()
	if request.method == 'GET':
		form = SessionForm()
	else:
		# A POST request: Handle Form Upload
		form = SessionForm(request.POST) # Bind data from request.POST into a PostForm
	 
		# If data is valid, proceeds to create a new post and redirect the user
		if form.is_valid():
			s=form.save()
			return render_to_response('gps/session_form.html',{ 'form': form }, context_instance=RequestContext(request) )
		

	return render_to_response('gps/session_form.html',{ 'form': form }, context_instance=RequestContext(request) )

##
##
##

@login_required
def importsessions(request):
	
	mytest="TTTT"
	userprofile=UserProfile.objects.get(user_id = request.user.id)

	if request.method == 'GET':
		form = ImportSessions()
	else:
		# A POST request: Handle Request here
		form = ImportSessions(request.POST) # Bind data from request.POST into a PostForm
			
		
		#do all the work here

		repat=re.compile('<.*?>')

		# test if user already has any sessions, if so just read in the current years ones.
		currentyear= timezone.now().year
		yearfilter="&year=" + str(currentyear)
	
		try: 
			s=Session.objects.get(user_id = request.user.id )
			# 1 record found - thats enough
			
		except Session.MultipleObjectsReturned:
			# more than 1 found - also enough
			s=""
			
		except Session.DoesNotExist:
			# only case where we get everthing.
			yearfilter=""

		url="http://www.gpsteamchallenge.com.au/sailor_session/export_session_csv?sailor_id=" + str(userprofile.gpstc_sailor_id) + yearfilter 
		print url

		try: 
			ftpstream = urllib2.urlopen(url)
			data=ftpstream.read().decode('utf-8')
		except:
			print "oops an error occurred opening the url"
			data=""

		fdata=StringIO.StringIO(data)
		csvfile=csv.reader(fdata)
		readcnt=0
		errcnt=0
		impcnt=0
		fndcnt=0
		
		for r in csvfile:
			if ( r[0]=="FullName" ):
				print "firstline found ignore this one."
			else:
				try: 
					newsess=Session()
					newsess.user_id=request.user.id
					newsess.FullName=r[0]
					newsess.NickName=r[1]
					print r[2]
					newsess.SessionDate=datetime.strptime(r[2],'%d %b %Y')

					print newsess.SessionDate
					newsess.Team=r[3]
					newsess.Age_Division=r[4]
					newsess.Two_Second_Peak=float(r[5])
					newsess.Two_Second_Peak_Method=r[6]
					newsess.Five_X_10_Second_Average=float(r[7])
					newsess.Five_X_10_Second_Average_Method=r[8]
					newsess.One_Hour=float(r[9])
					newsess.One_Hour_Method=r[10]
					newsess.Alpha_Racing_500m=float(r[11])
					newsess.Alpha_Racing_500m_Method=r[12]
					newsess.Nautical_Mile=float(r[13])
					newsess.Nautical_Mile_Method=r[14]
					newsess.Distance_Travelled=float(r[15])
					newsess.Distance_Travelled_Method=r[16]
					newsess.Comments=repat.sub('',r[17].replace('&nbsp;',''))

					readcnt+=1
					err=0
				except :
					print "oops issue in converting csv", sys.exc_info()[0]
					err=1
					errcnt+=1

				if (err == 0 ) :
					try:
						#search for existing record
						try:
							ifexist=Session.objects.get(user_id=newsess.user_id, SessionDate=newsess.SessionDate)
							fndcnt+=1
						except Session.MultipleObjectsReturned:
							fndcnt+=1
						except Session.DoesNotExist:
							newsess.save()
							impcnt+=1
					except:
						errcnt+=1
					
				
		print readcnt
		#pdb.set_trace()
		#return HttpResponseRedirect(('ImportSessonsResult'))
		#return HttpResponseRedirect(reverse('importsessionsresult', kwargs={'form': form, 'user': request.user , 'userprofile':userprofile, 'items_read':readcnt, 'items_with_errors':errcnt, 'items_found':fndcnt, 'items_added':impcnt }))
		return HttpResponseRedirect( reverse('importsessionsresult', kwargs={'userprofileid': userprofile.gpstc_sailor_id, 'items_read': readcnt, 'items_with_errors': errcnt, 'items_found': fndcnt, 'items_added': impcnt, } ) )

		#return render_to_response('gps\importsessionsresult.html',{ 'form': form, 'user': request.user , 'userprofile':userprofile, 'items_read':readcnt, 'items_with_errors':errcnt, 'items_found':fndcnt, 'items_added':impcnt }, context_instance=RequestContext(request) )

	return render_to_response('gps/importsessions.html',{ 'form': form, 'user': request.user , 'userprofile':userprofile }, context_instance=RequestContext(request) )


##
##
##

@login_required
def importsessionsresult(request,items_read, items_added, items_with_errors, items_found, userprofileid ):
	return render_to_response('gps/importsessionsresult.html', {'request': request ,  'userprofileid': userprofileid ,'items_read':items_read , 'items_with_errors': items_with_errors , 'items_found': items_found , 'items_added': items_added  } , context_instance=RequestContext(request) )


##
##
##

@login_required
def getsailorid(request):

	userprofile=UserProfile.objects.get(user_id = request.user.id)

	if request.method == 'GET':
		form = GetSailorID(initial={'my_message':getsailoridmymessage})
		
	
	else:
		# A POST request: Handle Request here
		form = GetSailorID(request.POST) # Bind data from request.POST into a PostForm
		pdb.set_trace()
		
		#do all the work here


		url="http://gpsteamchallenge.com.au/sailor_session/mydata/" + str(userprofile.gpstc_sailor_id)  

		print url
		pdb.set_trace()
		try: 
			webstream = urllib2.urlopen(url)
			data=webstream.read().decode('utf-8')
		except:
			print "oops an error occurred opening the url"
			data=""

		fdata=StringIO.StringIO(data)
		print data
		
		pdb.set_trace()
		#ValidationError(_('Validation error'),code='invalid')

		return HttpResponseRedirect( reverse('getsailorid' ) )

		#return HttpResponseRedirect( reverse('getsailorid', kwargs={'userprofileid': userprofile.gpstc_sailor_id, } ) )

	return render_to_response('gps/getsailorid.html',{ 'form': form, 'user': request.user , 'userprofile':userprofile }, context_instance=RequestContext(request) )




##
##
##



@login_required
def processsessions(request):

	userprofile=UserProfile.objects.get(user_id = request.user.id)

	if request.method == 'GET':
		pdb.set_trace()
		
		my_message=''
		myequip=Equipment.objects.filter(user_id = request.user.id )
		
        	for s in Session.objects.filter(user_id = request.user.id ): 
			#my_message=my_message + '\n' +  s.Comments
			for e in myequip:
				#print e.KeyWords
				wrds=e.KeyWords.upper().split(';')
				if len(wrds) >= 1 :
					for w in wrds:
						if w in s.Comments.upper():
							#pdb.set_trace()
							try:
								got1=SessionEquipment.objects.get(Session_id=s.id , Equipment_id=e.id)
							except SessionEquipment.MultipleObjectsReturned:
								pass
							
							except SessionEquipment.DoesNotExist:
								print w,' created ',s,e
								newse=SessionEquipment()
								newse.Session_id=s.id
								newse.Equipment_id=e.id
								newse.save()

		
		form = ProcessSessionsForm(initial={'my_user':userprofile.user_id, 'my_message':my_message })
	
		
	else:
		# A POST request: Handle Request here

		form = ProcessSessionsForm(request.POST)
		print form.is_valid()
		#	return HttpResponseRedirect( '..' ) 



	return render_to_response('gps/processsessions.html', {'form': form , 'user': request.user , 'userprofile':userprofile  } , context_instance=RequestContext(request) )



