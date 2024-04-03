from django.contrib.auth.models import AbstractUser,BaseUserManager
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
import re
from django.conf import settings
from django.utils.safestring import mark_safe
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import datetime
from django.template.defaultfilters import linebreaksbr, striptags
from django.utils.html import escape


class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        JOBSEEKER = "JOBSEEKER", "jobseeker"
        EMPLOYEER = "EMPLOYEER", "employeer"
        MODERATOR = "MODERATOR", "moderator"

    base_role = Role.ADMIN
    role = models.CharField(max_length=50, choices=Role.choices)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.role = self.base_role
            return super().save(*args, **kwargs)



class JobseekerManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role=User.Role.JOBSEEKER)


class Jobseeker(User):
    base_role = User.Role.JOBSEEKER
    student = JobseekerManager()
    class Meta:
        proxy = True

    def welcome(self):
        return "Only for students"


@receiver(post_save, sender=Jobseeker)
def create_user_profile(sender, instance, created, **kwargs):
    if created and instance.role == "JOBSEEKER":
        JobseekerProfile.objects.create(user=instance)
        # PayementDetails.objects.create(profile=instance)

class JobseekerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # jobseeker_id = models.IntegerField(null=True, blank=True)
    first_name = models.CharField(null=True,blank=True,max_length=100)
    last_name = models.CharField(null=True,blank=True,max_length=100)
    phone_number = models.CharField(blank=True, null=True,max_length=15)
    email=models.EmailField(blank=True, null=True,max_length=60)
    highestqualification=models.CharField(blank=True, null=True,max_length=50)
    experience=models.CharField(blank=True, null=True,max_length=15)
    skills=models.CharField(blank=True, null=True,max_length=15)
    cgpa=models.CharField(blank=True, null=True,max_length=15)
    age=models.IntegerField(blank=True, null=True)
    profile_photo = models.ImageField(null=True,blank=True,upload_to='images/')
    aboutyourself = models.CharField(null=True,blank=True,max_length=600)
    fulladdress= models.CharField(null=True,blank=True,max_length=500)

    
    def __str__(self):
        return str(self.first_name)


class candidateSkillsandTechnologies(models.Model):
    skill_name = models.CharField(max_length=50,null=True,blank=True)
    profile_id = models.ForeignKey(JobseekerProfile,default=None,on_delete=models.CASCADE)




#Employeer Models

class EmployeerManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role=User.Role.EMPLOYEER)


class Employeer(User):

    base_role = User.Role.EMPLOYEER
    employeer = EmployeerManager()

    class Meta:
        proxy = True

    def welcome(self):
        return 



def validate_phone_number(value):
    if not re.match(r'^\d{10}$', value):
        raise ValidationError(_('Invalid phone number format'))

class EmployeerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # employeer_id = models.IntegerField(null=True, blank=True)
    company_name = models.CharField(null=True,blank=True,max_length=100)
    office_location = models.CharField(null=True,blank=True,max_length=100)
    address = models.CharField(max_length=255,null=True,blank=True)
    # pincode = models.IntegerField(blank=True, null=True)
    # website_url = models.URLField(blank=True, null=True)
    phone_number = models.CharField(blank=True, null=True,max_length=15,validators=[validate_phone_number])
    company_logo = models.ImageField(null=True,blank=True,upload_to='images/')
    
    

    def __str__(self):
        return str(self.user)
    

class Verificationdetails(models.Model):
    user = models.OneToOneField(User,default=None,on_delete=models.CASCADE)
    buisnesslicence=models.ImageField(null=True,blank=True,upload_to='images/')
    isverified=models.BooleanField('isverified',default=0)

@receiver(post_save, sender=Employeer)
def create_user_profile_and_verification_details(sender, instance, created, **kwargs):
    if created and instance.role == "EMPLOYEER":
        EmployeerProfile.objects.create(user=instance)
        Verificationdetails.objects.create(user=instance)

class Jobdetails(models.Model):
    job_id = models.AutoField(primary_key=True)
    job_title = models.CharField(max_length=100)
    job_description = models.CharField(max_length=500)
    contact_email = models.CharField(max_length=100)
    job_type = models.CharField(max_length=100)
    specialisation = models.CharField(max_length=100)
    experience = models.IntegerField(blank=True, null=True)
    # expected_salary = models.CharField(max_length=100)
    # qualification = models.CharField(max_length=100)
    vacancies = models.IntegerField(blank=True, null=True)
    lastdate =  models.DateField()
    cmp_id = models.ForeignKey(User,default=None,on_delete=models.CASCADE)
    publisheddate = models.DateTimeField(default=datetime.date.today)
    office_location = models.CharField(max_length=100, default="")
    # cmp_profile = models.ForeignKey(EmployeerProfile,default=None,on_delete=models.CASCADE)




#Job application details

class JobapplicationDetails(models.Model):
    application_id = models.AutoField(primary_key=True)
    jobseekerprofile = models.ForeignKey(JobseekerProfile, default=None, on_delete=models.CASCADE)
    job = models.ForeignKey(Jobdetails, default=None, on_delete=models.CASCADE)
    employerprofile = models.ForeignKey(EmployeerProfile, default=None, on_delete=models.CASCADE)
    applicant_resume = models.FileField(null=True, blank=True, upload_to='pdf/')
    application_status = models.BooleanField('status', default=1)


class ResumeSchema(models.Model):

    YEAR_CHOICES = [(year, year) for year in range(1900, 2100)]

    resume_id=models.AutoField(primary_key=True)
    resumetitle=models.CharField(max_length=500,null=True,blank=True)
    jprofile = models.ForeignKey(JobseekerProfile, default=None, on_delete=models.CASCADE)
    seekername=models.CharField(max_length=100,null=True,blank=True)
    careerobjective=models.CharField(max_length=500,null=True,blank=True)
    profilepicture= models.FileField(null=True, blank=True, upload_to='resumeprofile/')
    projecttitle=models.CharField(max_length=100,null=True,blank=True)
    projectdescription=models.CharField(max_length=500,null=True,blank=True)
    address=models.CharField(max_length=255,null=True,blank=True)
    phonenumber=models.CharField(blank=True, null=True,max_length=15)
    collegename=models.CharField(max_length=255,null=True,blank=True)
    coursename=models.CharField(max_length=255,null=True,blank=True)
    passingyear = models.CharField(max_length=4,null=True,blank=True)
    hssname=models.CharField(max_length=255,null=True,blank=True)
    hssmarks=models.CharField(max_length=255,null=True,blank=True)
    hssyear = models.CharField(max_length=4,null=True,blank=True)
    tenthschoolname=models.CharField(max_length=255,null=True,blank=True)
    tenthpassyear = models.CharField(max_length=4,null=True,blank=True)
    tenthmarks=models.CharField(max_length=255,null=True,blank=True)
    email=models.EmailField(blank=True,null=True)
    skills=models.CharField(blank=True,null=True,max_length=200)

    def __str__(self):
        return self.resumetitle

class PayementDetails(models.Model):
    user_name=models.CharField(max_length=255,null=True,blank=True)
    profile=models.OneToOneField(User, on_delete=models.CASCADE,null=True)
    amount=models.CharField(max_length=100,null=True,blank=True)
    order_id=models.CharField(max_length=255,null=True,blank=True)
    razorpay_payment_id=models.CharField(max_length=100,null=True,blank=True)
    paid=models.BooleanField(default=False)
    productname=models.CharField(max_length=100,null=True,blank=True)

class Interviewscheduling(models.Model):
    interview_id=models.AutoField(primary_key=True)
    time_duration=models.CharField(max_length=255,null=True,blank=True)
    interview_type=models.CharField(max_length=255,null=True,blank=True)
    interview_timeanddate=models.DateTimeField(null=True,blank=True)
    application=models.ForeignKey(JobapplicationDetails,default=None, on_delete=models.CASCADE)
    job=models.ForeignKey(Jobdetails,default=None, on_delete=models.CASCADE)
    status=models.BooleanField('status', default=0)
    message=models.TextField(max_length=255,null=True,blank=True)
    interviewlink=models.URLField(max_length=255,null=True,blank=True)



class feedback(models.Model):
    f_id = models.AutoField(primary_key=True)
    can_id = models.ForeignKey(User ,default=None,on_delete=models.CASCADE)
    status=models.BooleanField('status', default=True) 
    feedback=models.TextField(null=True)
    percentage=models.FloatField(blank=True, null=True)
    good=models.BooleanField('good', default=True)
    bad=models.BooleanField('bad', default=True)
    neutral=models.BooleanField('neutral', default=True)
    rating=models.CharField(max_length=100,null=True,)


    @property
    def username(self):
        return self.can_id.username

from django.db import models
from django.utils import timezone

class Interndetails(models.Model):
    title = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    description = models.TextField()
    duration = models.CharField(max_length=50)
    location = models.CharField(max_length=100)
    mode = models.CharField(max_length=50)
    stipend = models.CharField(max_length=50, default="2000")
    whocanapply = models.CharField(max_length=100, default="CS related")
    startdate = models.DateField(default=timezone.now)  # Set default value to current date
    lastdate = models.DateField(default=timezone.now)   # Set default value to current date

    def __str__(self):
        return self.title


    # cmp_profile = models.ForeignKey(EmployeerProfile,default=None,on_delete=models.CASCADE)   
# class internship(models.Model):
#     intern_id = models.AutoField(primary_key=True)
#     status=models.BooleanField('status', default=True) 
#     title=models.CharField(max_length=100,null=True)
#     durno = models.IntegerField(blank=True, null=True)
#     durex = models.CharField(max_length=100,null=True)
#     stdate =  models.DateField()
#     enddate =  models.DateField()
#     caption=models.CharField(max_length=100,null=True)
#     img=models.ImageField(null=True,blank=True,upload_to="img/")
#     category=models.CharField(max_length=100,null=True)
#     stipend=models.IntegerField(blank=True, null=True)
#     location=models.CharField(max_length=100,null=True)
#     moreinfo=models.TextField(null=True)
#     whoapply=models.TextField(null=True)
#     onoff=models.CharField(max_length=100,null=True)
#     certificate=models.BooleanField('status', default=True) 
#     tim=models.CharField(max_length=100,null=True)

# class interdetails(models.Model):
#     in_id=models.AutoField(primary_key=True)
#     cann_id=models.IntegerField(blank=True, null=True)
#     status=models.BooleanField('status', default=False) 
#     interns=models.CharField(max_length=100,null=True)
#     internname=models.CharField(max_length=100,null=True)
#     interndate=models.DateField()

# from datetime import datetime

# class classdetails(models.Model):
#     in_id=models.AutoField(primary_key=True)
#     status=models.BooleanField('status', default=True) 
#     candi_id=models.ForeignKey(User ,default=None,on_delete=models.CASCADE)
#     inter_id=models.ForeignKey(internship ,default=None,on_delete=models.CASCADE)
#     interndate =  models.DateField(default=datetime.now, blank=True)
#     interntimes = models.CharField(max_length=100,null=True,default=0)
    
#     @property
#     def canid(self):
#       return self.candi_id.id
    
#     @property
#     def inid(self):
#       return self.inter_id.title
    
# models.py

