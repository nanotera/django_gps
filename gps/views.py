# Create your views here.
#from django.forms import ModelForm
from django.shortcuts import render
from django.template import Context, loader
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse

from django.contrib.auth.decorators import login_required

from gps.forms import SessionForm, ImportSessions, GetSailorID, ProcessSessionsForm,  ProcessSessionsFormConfirm
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
## takes one csv line, user_id,  a regular expression for cleanup of comments and returns a Session object.
##
def process_line(my_line,my_user,  regexp):


	try:

		newsess=Session()
		newsess.user_id=my_user
		newsess.FullName=my_line[0]
		newsess.NickName=my_line[1]
		print my_line[2]
		newsess.SessionDate=datetime.strptime(my_line[2],'%d %b %Y')
		#print newsess.SessionDate
		newsess.Team=my_line[3]
		newsess.Age_Division=my_line[4]
		newsess.Two_Second_Peak=float(my_line[5])
		newsess.Two_Second_Peak_Method=my_line[6]
		newsess.Five_X_10_Second_Average=float(my_line[7])
		newsess.Five_X_10_Second_Average_Method=my_line[8]
		newsess.One_Hour=float(my_line[9])
		newsess.One_Hour_Method=my_line[10]
		newsess.Alpha_Racing_500m=float(my_line[11])
		newsess.Alpha_Racing_500m_Method=my_line[12]
		newsess.Nautical_Mile=float(my_line[13])
		newsess.Nautical_Mile_Method=my_line[14]
		newsess.Distance_Travelled=float(my_line[15])
		newsess.Distance_Travelled_Method=my_line[16]
		# convert comment by removing html codes (should probably do ' chars as well)
		newsess.Comments=regexp.sub('',my_line[17].replace('&nbsp;',''))
	
	except:

		newsess=None

	return newsess
##
##
##

@login_required
def importsessions(request):
	
	userprofile=UserProfile.objects.get(user_id = request.user.id)

	if request.method == 'GET':
		form = ImportSessions()
	else:
		# A POST request: Handle Request here
		form = ImportSessions(request.POST) # Bind data from request.POST into a PostForm
			
		if form.is_valid():
			#pass
			#pdb.set_trace()
			#do all the work here
			# test if user already has any sessions, if so just read in the current years ones.
			currentyear= timezone.now().year
			yearfilter="&year=" + str(currentyear)
	
			try: 
				s=Session.objects.get(user_id = request.user.id )
				# 1 record found - thats enough
			except Session.MultipleObjectsReturned:
				# more than 1 found - also enough
				pass
			except Session.DoesNotExist:
				# only case where we get everthing.
				yearfilter=""

			url="http://www.gpsteamchallenge.com.au/sailor_session/export_session_csv?sailor_id=" + str(userprofile.gpstc_sailor_id) + yearfilter 
			#print url
			try: 
				ftpstream = urllib2.urlopen(url)
				data=ftpstream.read().decode('utf-8')
			except:
				print "oops an error occurred opening the url"
				# Do a form error here
				pdb.set_trace()
				form._errors['']= form.error_class('error added')
				data=""

			# move data to a memory file as reading into csv fails direct from url.
			fdata=StringIO.StringIO(data)
			csvfile=csv.reader(fdata)
			readcnt=0
			errcnt=0
			impcnt=0
			fndcnt=0
			repat=re.compile('<.*?>')
		
		
			for r in csvfile:
				if ( r[0]=="FullName" ):
					print "firstline found ignore this one."
				else:
					### process the csv line in function.
					newsess=process_line(r, request.user.id, repat)
					####
					if newsess != None : 
						readcnt+=1
						try:
							ifexist=Session.objects.get(user_id=newsess.user_id, SessionDate=newsess.SessionDate)
							fndcnt+=1
						except Session.MultipleObjectsReturned:
							fndcnt+=1
						except Session.DoesNotExist:
							newsess.save()
							impcnt+=1
						except: # catch any other error here
							errcnt+=1

					else :
						print "oops issue in converting csv", sys.exc_info()[0]
						errcnt+=1
				
			#print 'records read %d ' % ( readcnt )
			#pdb.set_trace()
			return HttpResponseRedirect( reverse('importsessionsresult', kwargs={'userprofileid': userprofile.gpstc_sailor_id, 'items_read': readcnt, 'items_with_errors': errcnt, 'items_found': fndcnt, 'items_added': impcnt, } ) )

		else:
			print 'form invalid go round again'
			#pdb.set_trace()
		
	return render_to_response('gps/importsessions.html',{ 'form': form, 'user': request.user , 'userprofile':userprofile }, context_instance=RequestContext(request) )


##
##	importsessionsresult = displays message regarding import 
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
##	processsessionsconfirm - asked user to process sessions, allowed to select options. 
##

@login_required
def processsessionsconfirm( request ):
	userprofile=UserProfile.objects.get(user_id = request.user.id)
	
	#print request.method
	#pdb.set_trace()
	my_message='Confirm processing of sessions for user :'
	
	if request.method == 'GET':
		form = ProcessSessionsFormConfirm(initial={'my_user':userprofile.user_id, 'my_message':my_message })

	else:
		# A POST request: Handle Request here
		form = ProcessSessionsFormConfirm(request.POST)
		if form.is_valid():
			request.session['my_process_equipment']=form['my_process_equipment'].value()
			request.session['my_process_location']=form['my_process_location'].value()
			request.session['my_country']=form['my_country'].value()
			request.session['my_country']=form['my_country'].value()
			request.session['my_state']=form['my_state'].value()
			return HttpResponseRedirect( 'processsessions'  ) 


	return render_to_response('gps/processsessionsconfirm.html', {'form': form , 'user': request.user , 'userprofile':userprofile  } , context_instance=RequestContext(request) )


##
## 	processsessionsequipment - do keyword lookup of equipment in session comments
##
def processsessionsequipment(my_session,my_equipment):
	count={'found':0,'new':0}
	regex_left=r'([\s\W]|^)'
	regex_right =r'([\s\W\n]|$)'

	mycomment=my_session.Comments.upper()
	for e in my_equipment:
		#print e.KeyWords
		wrds=e.KeyWords.upper().split(';')
		if len(wrds) >= 1 :
			for w in wrds:
				p=re.compile(regex_left+w+regex_right)
				#print regex_left+w+regex_right
				pmatch=p.search(mycomment)
				if pmatch :
				
					try:
						got1=SessionEquipment.objects.get(Session_id=my_session.id , Equipment_id=e.id)
						count['found']+=1
					
					except SessionEquipment.MultipleObjectsReturned:
						count['found']+=1
						pass
				
					except SessionEquipment.DoesNotExist:
						count['new']+=1
						newse=SessionEquipment()
						newse.Session_id=my_session.id
						newse.Equipment_id=e.id
						newse.save()
				
	return count

##
##	processsessionslocation - do keyword lookup of Locations in session comments
##

def processsessionslocation(my_session,my_country, my_state ):
	count={'locfound':0,'locnew':0,'locchecked':0,'locations':0}
	print my_session.Location_id
	if my_session.Location_id == None :
		regex_left=r'([\s\W]|^)'
		regex_right =r'([\s\W\n]|$)'

		mycomment=my_session.Comments.upper()
		count['locchecked']+=1

		if my_country=='':
			if my_state=='':
				my_locs=Location.objects.all()
			else:
				my_locs=Location.objects.filter(State=my_state )
		else:
			if my_state=='':
				my_locs=Location.objects.filter( Country=my_country )
			else:
				my_locs=Location.objects.filter( Country=my_country , State=my_state )

		count['locations']=my_locs.count()
		for e in my_locs:
			#print e.KeyWords
			wrds=e.KeyWords.upper().split(';')
			if len(wrds) >= 1 :
				for w in wrds:
					p=re.compile(regex_left+w+regex_right)
					#print regex_left+w+regex_right
					pmatch=p.search(mycomment)
					if pmatch :
						print 'found', w
						my_session.Location_id=e.id
						my_session.save()
						count['locnew']+=1
						return count
	else:
		count['locfound']+=1
					
	return count


##
##	processsessions - checks sessions for included equipment and locations.
##


@login_required
def processsessions(request):

	userprofile=UserProfile.objects.get(user_id = request.user.id)
	
	#print request.method
	#pdb.set_trace()
	mycount={'sessions':0,'sessionsaltered':0,'found':0,'new':0,'locsessionsaltered':0,'locfound':0,'locnew':0,'locations':0,'locchecked':0, 'equipment':0}
		

	if request.method == 'GET':
		
		my_message=''
		if not (request.session['my_process_equipment'] or request.session['my_process_location']):
			my_message='Neither Equipment or Location selected to be processed, Nothing to do !'
		else:
			myequip=Equipment.objects.filter(user_id = request.user.id )
			mycount['equipment'], len(myequip)
	        	for s in Session.objects.filter(user_id = request.user.id ): 
				mycount['sessions']+=1
				if request.session['my_process_equipment']:
					scount=processsessionsequipment(s,myequip)
					mycount['found']+=scount['found']
					mycount['new']+=scount['new']
					if scount['new'] > 0:
						mycount['sessionsaltered']+=1
				if request.session['my_process_location']:
					scount=processsessionslocation(s, request.session['my_country'],request.session['my_state'])
					mycount['locfound']+=scount['locfound']
					mycount['locnew']+=scount['locnew']
					mycount['locchecked']+=scount['locchecked']
					if mycount['locations'] < scount['locations']:
						mycount['locations']=scount['locations']
					#print scount
					#pdb.set_trace()
 			
			
			my_message='Sessions examined %d altered %d equipment examined %d\n\n\tequipment matches found %d\n\tequipment matches created %d\n\n\tlocation matches already with locations %d found and added %d checked %d locations examined %d .' % ( mycount['sessions'] , mycount['sessionsaltered'], len(myequip) , mycount['found'] , mycount['new'], mycount['locfound'], mycount['locnew'], mycount['locchecked'], mycount['locations'] )
		
		request.session['mycount']=mycount
		form = ProcessSessionsForm(initial={'my_user':userprofile.user_id, 'my_message':my_message })
	
		
	else:
		# A POST request: Handle Request here
		#form = ProcessSessionsForm(request.POST)
		#print form.is_valid()
		#print request.POST
		return HttpResponseRedirect( '..' ) 


	pass
	return render_to_response('gps/processsessions.html', {'form': form , 'user': request.user , 'userprofile':userprofile  } , context_instance=RequestContext(request) )



