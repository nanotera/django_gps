from django.db import models
from django.contrib.auth.models import User

##
## userprofile table with extra data specific to this app
##

class UserProfile(models.Model):
    # This field is required.
    user = models.ForeignKey(User, unique=True)
    #user = models.OneToOneField(User, unique=True,primary_key=True,related_name="user")
    # Other fields here
    #accepted_eula = models.BooleanField()
    gpstc_sailor_id = models.DecimalField(max_digits=6, decimal_places=0 , default=0)
    gpstc_team_id = models.DecimalField(max_digits=6, decimal_places=0 , default=0)
    sailor_picture = models.ImageField(null=True)

    def __unicode__(self):
        return unicode(self.user)


##
## add new data when user registers
##

from registration.signals import user_registered
 
def user_registered_callback(sender, user, request, **kwargs):
    profile = UserProfile(user = user)
    try:
	profile.gpstc_sailor_id = request.POST["gpstc_sailor_id"]
	profile.gpstc_team_id = request.POST["gpstc_team_id"]
    except:
        profile.gpstc_sailor_id = 1

    profile.save()

user_registered.connect(user_registered_callback, dispatch_uid="gps_user_registered_callback")




##
## Models for GPS app 
##

class Session(models.Model):
        user = models.ForeignKey(User)
        FullName=models.CharField( 'FullName', max_length=32)
        NickName=models.CharField('NickName', max_length=32)
        SessionDate=models.DateField('SessionDate')
        Team=models.CharField('Team', max_length=40)
        Age_Division=models.CharField('Age Division', max_length=32)
        Two_Second_Peak=models.FloatField('2 Second Peak')
        Two_Second_Peak_Method=models.CharField('2 Second Peak Method', max_length=1)
        Five_X_10_Second_Average=models.FloatField('5 X 10 Second Average')
        Five_X_10_Second_Average_Method=models.CharField('5 X 10 Second Average Method', max_length=1)
        One_Hour=models.FloatField('1 Hour')
        One_Hour_Method=models.CharField('1 Hour Method', max_length=1)
        Alpha_Racing_500m=models.FloatField('Alpha Racing 500m')
        Alpha_Racing_500m_Method=models.CharField('Alpha Racing 500m Method', max_length=1)
        Nautical_Mile=models.FloatField('Nautical Mile')
        Nautical_Mile_Method=models.CharField('Nautical Mile Method', max_length=1)
        Distance_Travelled=models.FloatField('Distance Travelled')
        Distance_Travelled_Method=models.CharField('Distance Travelled Method', max_length=1)
        Comments=models.TextField('Comments')
        Location=models.ForeignKey('Location', null=True )
	KA72url=models.URLField(null=True)
	SessionImage = models.ImageField(null=True)

        def __unicode__(self):
                return self.SessionDate.isoformat()+' '+self.FullName+' '+self.NickName

##

class Location(models.Model):
        Name=models.CharField(max_length=20)
        Description=models.CharField(max_length=300)
        def __unicode__(self):
                return self.Name

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
        def __unicode__(self):
                return self.Name

##

class SessionEquipment(models.Model):
        Session=models.ForeignKey('Session')
        Equipment=models.ForeignKey('Equipment')
        def __unicode__(self):
                return self.Session.FullName+self.Equipment.Name


