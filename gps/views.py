# Create your views here.
#from django.forms import ModelForm
#from django.shortcuts import render
from django.template import Context, loader
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse

from django.contrib.auth.decorators import login_required

#class SessionForm(ModelForm):
#class Meta:
#model=Session
#fields='__all__'

from gps.forms import SessionForm, TestForm

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

def testform(request):
	if request.method == 'GET':
		form = TestForm()
	else:
		# A POST request: Handle Form Upload
		form = TestForm(request.POST) # Bind data from request.POST into a PostForm
	 
		# If data is valid, proceeds to create a new post and redirect the user
		if form.is_valid():
			#content = form.cleaned_data['content']
			#created_at = form.cleaned_data['created_at']
			#Session = m.Post.objects.create(content=content, created_at=created_at)
			s=form.save()
			#return HttpResponseRedirect(reverse('post_form_upload.html', kwargs={'Session_id': s.id}))
			return HttpResponseRedirect(('testform'))


	return render_to_response('gps/testform.html',{ 'form': form, }, context_instance=RequestContext(request) )

#return render_to_response(loader.get_template('gps/post_form_upload.html'),{ 'form': form, } )
#return HttpResponse(t.render(Context({ 'form': form, })))

#def index(request):
	#return HttpResponseRedirect(reverse("registration_register"))

