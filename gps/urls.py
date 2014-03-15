from django.conf.urls.defaults import *

from gps.models import Session , UserProfile

from gps.forms import ExRegistrationForm
from registration.backends.default.views import RegistrationView
 

info_dict = {
    'queryset': Session.objects.all(),
}


urlpatterns = patterns('',
	url(r'^register/$', RegistrationView.as_view(form_class = ExRegistrationForm), name = 'registration_register'), 
	(r'^$', 'django.views.generic.list_detail.object_list', info_dict),
	(r'^(?P<object_id>\d+)/$', 'django.views.generic.list_detail.object_detail', info_dict),
	url(r'^(?P<object_id>\d+)/results/$', 'django.views.generic.list_detail.object_detail', dict(info_dict, template_name='gps/'), 'session_list'),
	url(r'^importsessions$', 'gps.views.importsessions', name='importsessions'),
	url(r'importsessionsresult/(?P<items_added>\d+)/(?P<items_read>\d+)/(?P<items_with_errors>\d+)/(?P<items_found>\d+)/(?P<userprofileid>\d+)' , 'gps.views.importsessionsresult' , name='importsessionsresult')
	#url(r'importsessionsresult/(?P<items_read>\d{4})(?P<userprofileid>\{d4})' , 'gps.views.importsessions' , name='importsessionsresult')


)


