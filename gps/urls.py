from django.conf.urls.defaults import *
from registration.backends.default.views import RegistrationView
from django.conf.urls import patterns, include,  url
from django.views.generic import UpdateView, DetailView, ListView
from gps.models import Session , UserProfile

from gps.forms import ExRegistrationForm,GetSailorID, GetSailorIDFormPreview,ProcessSessionsForm
 

info_dict = {
    'queryset': Session.objects.all(),
}


urlpatterns = patterns('',
	url(r'^register/$', RegistrationView.as_view(form_class = ExRegistrationForm), name = 'registration_register'), 
	#url(r'list', 'gps.views.SessionsAsTable'),
	url(r'^$', 'gps.views.SessionsAsTable'),
	url(r'^(?P<pk>\d+)/$', UpdateView.as_view(queryset=Session.objects.all() , template_name = 'gps/session_form.html' , success_url='/' )),
	#url(r'^(?P<pk>\d+)/$', DetailView.as_view( model=Session, template_name = 'gps/session_form.html' )),

	#url(r'^(?P<object_id>\d+)/results/$', 'django.views.generic.list_detail.object_detail', dict(info_dict, template_name='gps/'), 'session_list'),
	url(r'^importsessions$', 'gps.views.importsessions', name='importsessions'),
	url(r'importsessionsresult/(?P<items_added>\d+)/(?P<items_read>\d+)/(?P<items_with_errors>\d+)/(?P<items_found>\d+)/(?P<userprofileid>\d+)' , 'gps.views.importsessionsresult' , name='importsessionsresult'),
	#url(r'importsessionsresult/(?P<items_read>\d{4})(?P<userprofileid>\{d4})' , 'gps.views.importsessions' , name='importsessionsresult')

	url(r'^getsailorid$', GetSailorIDFormPreview(GetSailorID), name='getsailorid'),
	url(r'^processsessions$', 'gps.views.processsessions', name='processsessions'),
	

)


