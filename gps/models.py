from django.db import models
from django.contrib.auth.models import User
from django.db.models.query import QuerySet

##
## userprofile table with extra data specific to this app
##

class UserProfile(models.Model):
    # This field is required.
    user = models.ForeignKey(User, unique=True)
    #user = models.OneToOneField(User, unique=True,primary_key=True,related_name="user")
    # Other fields here
    #accepted_eula = models.BooleanField()
    gpstc_sailor_id = models.DecimalField(max_digits=6, decimal_places=0 , default=0, help_text='Numeric sailor-id used in GPSTC web site.')
    gpstc_team_id = models.DecimalField(max_digits=6, decimal_places=0 , default=0, help_text='Numeric team-id used in GPSTC web site.')
    FullName =models.CharField('Name', max_length=40,help_text='Sailors full name used in GPSTC web site.')
    NickName =models.CharField('NickName', max_length=40,help_text='Sailors Nickname used in GPSTC web site.')
    sailor_picture = models.ImageField(null=True, blank=True, upload_to='sailor_picture')
    Country=models.CharField(max_length=2,help_text='Default Country for locations.')
    State=models.CharField(max_length=20,help_text='Default State for locations.')

    def __unicode__(self):
        return unicode(self.user)


##
## add new data when user registers
##

from registration.signals import user_registered
 
def user_registered_callback(sender, user, request, **kwargs):
    profile = UserProfile( user = user )
    try:
    	profile.gpstc_sailor_id = request.POST["gpstc_sailor_id"]
    	profile.gpstc_team_id = request.POST["gpstc_team_id"]
	profile.FullName=request.POST["FullName"]
	profile.NickName=request.POST["NickName"]
    except:
        profile.gpstc_sailor_id = 0
	profile.gpstc_team_id=0
	profile.FullName=''
	profile.NickName=''
    profile.save()

user_registered.connect(user_registered_callback, dispatch_uid="gps_user_registered_callback")




##
## Models for GPS app 
##

#class QuerySetManager(models.Manager):
#	def get_query_set(self):
#		return self.model.QuerySet(self.model)
#	def __getattr__(self, attr, *args):
#		return getattr(self.get_query_set(), attr, *args)





class Session(models.Model):
        user = models.ForeignKey(User)
        FullName=models.CharField( 'FullName', max_length=32)
        NickName=models.CharField('NickName', max_length=32)
        SessionDate=models.DateField('Date')
        Team=models.CharField('Team', max_length=40)
        Age_Division=models.CharField('Age Division', max_length=32)
        Two_Second_Peak=models.FloatField('2 Sec')
        Two_Second_Peak_Method=models.CharField('2 Second Peak Method', max_length=1)
        Five_X_10_Second_Average=models.FloatField('5X10')
        Five_X_10_Second_Average_Method=models.CharField('5 X 10 Second Average Method', max_length=1)
        One_Hour=models.FloatField('1 Hour')
        One_Hour_Method=models.CharField('1 Hour', max_length=1)
        Alpha_Racing_500m=models.FloatField('Alpha')
        Alpha_Racing_500m_Method=models.CharField('Alpha Racing 500m Method', max_length=1)
        Nautical_Mile=models.FloatField('NMile')
        Nautical_Mile_Method=models.CharField('Nautical Mile Method', max_length=1)
        Distance_Travelled=models.FloatField('Distance')
        Distance_Travelled_Method=models.CharField('Distance Travelled Method', max_length=1)
        Comments=models.TextField('Comments')
        Location=models.ForeignKey('Location', null=True )
	KA72url=models.URLField(null=True,blank=True)
	SessionImage = models.ImageField(null=True,blank=True,upload_to='sessionimage')
	#objects=QuerySetManager()

	#class QuerySet(QuerySet):
	#	def SessionEditableFields(self):
	#		return self.values('FullName','SessionDate')

        def __unicode__(self):
		myloc=self.Location_id
		if myloc:
			myloc=self.Location.Name
		else:
			myloc="unknown location"
                return self.SessionDate.isoformat()+' '+self.NickName+' ' + myloc




class Location(models.Model):
        Name=models.CharField(max_length=20,unique=True)
        State=models.CharField(max_length=4,blank=True,default='')
        Country=models.CharField(max_length=2,blank=True,default='')
        Description=models.CharField(max_length=40)
        KeyWords=models.CharField(max_length=300,null=True,blank=True,help_text='List of words seperated by ; characters, used to match to session comments.')
	def __unicode__(self):
                return self.Name
	class Meta:
		ordering=['Name']

##

EQUIPMENT_TYPE_CHOICES=(
        ('Board',"Board"),
        ('Sail','Sail'),
        ('Fin','Fin'),
        ('Other','Other'),
)

##

class Equipment(models.Model):
        user = models.ForeignKey(User)
        Name=models.CharField(max_length=20)
        Description=models.CharField(max_length=300)
        Type=models.CharField(max_length=8,choices=EQUIPMENT_TYPE_CHOICES)
        KeyWords=models.CharField(max_length=300,null=True,blank=True,help_text='List of words seperated by ; characters, used to match to session comments.')
	def __unicode__(self):
                return self.Name+' '+self.Type
	class Meta:
		ordering=['Name']

##

class SessionEquipment(models.Model):
        Session=models.ForeignKey('Session')
        Equipment=models.ForeignKey('Equipment')
        def __unicode__(self):
                return self.Session.SessionDate.isoformat()+' '+self.Equipment.Name


