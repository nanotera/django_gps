from gps.models import Session,Location,Equipment,SessionEquipment

from gps.models import UserProfile


from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from django import forms
import pdb



admin.site.register(Location)

class EquipmentAdmin(admin.ModelAdmin):
	##
	## return only session records owned by this user
	##
	def queryset(self, request):
		qs=Equipment.objects.all()
		if request.user.is_superuser:
			return qs
		return qs.filter(user_id=request.user.id)

	def formfield_for_dbfield(self, field, **kwargs):
		print field.name
		#pdb.set_trace()
		if not(kwargs['request'].user.is_superuser) and field.name=='user':
		
			qs =User.objects.all().filter(id=kwargs['request'].user.id)
			kwargs['queryset']=qs
		return super(EquipmentAdmin, self).formfield_for_dbfield(field, **kwargs)


admin.site.register(Equipment,EquipmentAdmin)

admin.site.register(SessionEquipment)

class SessionEquipmentInline(admin.TabularInline):
	model = SessionEquipment
	extra = 3
	#form=SessionEquipmentForm
	##
	## return only equipment records owned by this user
	##
	
	def formfield_for_dbfield(self, field, **kwargs):
			print field.name
			if not(kwargs['request'].user.is_superuser) and field.name=='Equipment':
				#pdb.set_trace()
				qs =Equipment.objects.all().filter(user_id=kwargs['request'].user.id)
				kwargs['queryset']=qs
			return super(SessionEquipmentInline, self).formfield_for_dbfield(field, **kwargs)
	
class SessionAdmin(admin.ModelAdmin):
	fieldsets = [
		(None,               {'fields': (('FullName','NickName','SessionDate',),)}),
		#('Date information', {'fields': ['SessionDate'], 'classes': ['collapse']}),
		#( None,               {'fields': ['NickName']}),
		(None,               {'fields': (('Two_Second_Peak','Five_X_10_Second_Average','Alpha_Racing_500m','Nautical_Mile','One_Hour','Distance_Travelled'),),'classes':['gpstc_data'],}),
		(None,               {'fields': (('Location','Comments'),)}),
		
	]
	inlines = [SessionEquipmentInline]
	list_filter = ['Location']

	##
	## return only session records owned by this user
	##
	def queryset(self, request):
		qs=Session.objects.all()
		if request.user.is_superuser:
			return qs
		return qs.filter(user_id=request.user.id)


admin.site.register(Session,SessionAdmin)


# Define an inline admin descriptor for UserProfile model
# which acts a bit like a singleton
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    
# Define a new User admin
class UserAdmin(UserAdmin):
    inlines = (UserProfileInline, )

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

admin.site.register(UserProfile)


