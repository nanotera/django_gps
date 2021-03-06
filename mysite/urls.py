from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.contrib.auth.views import login
from django.views.generic.simple import direct_to_template

from gps.forms import ExRegistrationForm
from registration.backends.default.views import RegistrationView

admin.autodiscover()

urlpatterns = patterns('',
	# Examples:
	# url(r'^$', 'mysite.views.home', name='home'),
	# url(r'^mysite/', include('mysite.foo.urls')),
	url(r'^gps/', include('gps.urls')),

	# Uncomment the admin/doc line below to enable admin documentation:
	url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

	# Uncomment the next line to enable the admin:
	url(r'^admin/', include(admin.site.urls)),
        
	url(r'^accounts/register/$', RegistrationView.as_view(form_class = ExRegistrationForm), name = 'registration_register'),
	url(r'^accounts/',include('registration.backends.default.urls')),
	
	(r'^$', direct_to_template, { 'template': 'index.html' }, 'index'),

  
)
