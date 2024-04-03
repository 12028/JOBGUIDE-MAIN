from django.contrib import admin

# Register your models here.

from .models import User,EmployeerProfile,feedback,Interviewscheduling,PayementDetails,ResumeSchema,Verificationdetails,Jobdetails,Interndetails,JobseekerProfile,candidateSkillsandTechnologies
from .models import JobapplicationDetails

admin.site.register(User)
admin.site.register(EmployeerProfile)
admin.site.register(Verificationdetails)
admin.site.register(Jobdetails)
admin.site.register(Interndetails)
# admin.site.register(internship)
admin.site.register(feedback)
admin.site.register(ResumeSchema)

admin.site.register(JobseekerProfile)
admin.site.register(PayementDetails)
admin.site.register(Interviewscheduling)
admin.site.register(candidateSkillsandTechnologies)

admin.site.register(JobapplicationDetails)