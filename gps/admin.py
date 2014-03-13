from gps.models import Session,Location,Equipment,SessionEquipment

from gps.models import UserProfile


from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User



admin.site.register(Location)
admin.site.register(Equipment)
admin.site.register(SessionEquipment)

class SessionEquipmentInline(admin.TabularInline):
    model = SessionEquipment
    extra = 3

class SessionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['FullName']}),
        (None,               {'fields': ['NickName']}),
        (None,               {'fields': ['Location']}),
        ('Date information', {'fields': ['SessionDate'], 'classes': ['collapse']}),
    ]
    inlines = [SessionEquipmentInline]
    list_filter = ['Location']
    #list_display = ('equipment')

#admin.site.register(SessionEquipment ,SessionEquipmentAdmin )
#admin.site.register(Session,SessionAdmin)

admin.site.register(Session)


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

