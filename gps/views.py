# Create your views here.
#from django.forms import ModelForm
#from django.shortcuts import render
from django.template import Context, loader
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse

from django.contrib.auth.decorators import login_required

from gps.forms import SessionForm, ImportSessions

from gps.models import UserProfile
from gps.models import Session

@login_required
def post_form_upload(request):
	if request.method == 'GET':
		form = SessionForm()
	else:
		# A POST request: Handle Form Upload
		form = SessionForm(request.POST) # Bind data from request.POST into a PostForm
	 
		# If data is valid, proceeds to create a new post and redirect the user
		if form.is_valid():
			#content = form.cleaned_data['content']
			#created_at = form.cleaned_data['created_at']
			#Session = m.Post.objects.create(content=content, created_at=created_at)
			s=form.save()
			#return HttpResponseRedirect(reverse('post_form_upload.html', kwargs={'Session_id': s.id}))
			return HttpResponseRedirect(('post_form_upload.html'))


	return render_to_response('gps/post_form_upload.html',{ 'form': form, 'name': request.user.username, }, context_instance=RequestContext(request) )

@login_required
def importsessions(request):
	
	import pdb
	userprofile=UserProfile.objects.get(user_id = request.user.id)


	if request.method == 'GET':
		form = ImportSessions()
	else:
		# A POST request: Handle Form Upload
		form = ImportSessions(request.POST) # Bind data from request.POST into a PostForm
	 
		# If data is valid, proceeds to create a new post and redirect the user
		if form.is_valid():
			#content = form.cleaned_data['content']
			#created_at = form.cleaned_data['created_at']
			#Session = m.Post.objects.create(content=content, created_at=created_at)
			#s=form.save()
			#return HttpResponseRedirect(reverse('post_form_upload.html', kwargs={'Session_id': s.id}))

			#do all the work here
			import csv
			import urllib2
			import StringIO
			from datetime import datetime

			url="http://www.gpsteamchallenge.com.au/sailor_session/export_session_csv?sailor_id=" + str(userprofile.gpstc_sailor_id)
			
			ftpstream = urllib2.urlopen(url)

			data=ftpstream.read().decode('utf-8')
			fdata=StringIO.StringIO(data)
			csvfile=csv.reader(fdata)
			i=0
			errcnt=0
			impcnt=0
			pdb.set_trace()
			for r in csvfile:
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
					newsess.Comments=r[17]
					i=i+1
					err=0
				except:
					print "oops"
					pdb.set_trace()
					err=1
					errcnt=errcnt+1

				if (err == 0 ) :
					newsess.save()
					impcnt=impcnt+1
					
			print i
			#return HttpResponseRedirect(('ImportSessonsResult'))
			return render_to_response('gps/importsessionsresult.html',{ 'form': form, 'user': request.user , 'userprofile':userprofile, 'items_read':i, 'items_with_errors':errcnt, 'items_found':0, 'items_added':impcnt }, context_instance=RequestContext(request) )


	return render_to_response('gps/importsessions.html',{ 'form': form, 'user': request.user , 'userprofile':userprofile }, context_instance=RequestContext(request) )


