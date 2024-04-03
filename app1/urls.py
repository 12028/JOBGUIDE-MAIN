from django.urls import path
from django.contrib import admin
from django.urls import path
from . import views
from .views import *
from django.contrib.auth import views as auth_views
from django.urls import path
from .views import generate_pdf_report



urlpatterns = [
    path('',views.index, name='index'),
    path('login/',views.loginpage,name='loginpage'),
    path('jobseeker',views.jsregpage,name='jsregpage'),
    path('recruiter',views.rregpage,name='rregpage'),
    path('check_username/', views.check_username, name='check_username'),
    path('check_email/', views.check_email, name='check_email'),
    path('logout', views.logout_view, name='logout_view'),

#Different User Home Page Urls   
    path('adminpage/', views.adminpage, name='adminpage'),
    path('candidate', views.candidatepage, name='candidatepage'),
    path('employeer', views.employeerpage, name='employeerpage'),


#Employeer Page Urls
    path('postjob', views.postjob, name='postjob'),
    path('managejobs/<int:id>/',views.managejobs,name='managejobs'),




    
    path('deletejob/<int:id>/',views.deletejob,name='deletejob'),
    path('editjob/<int:id>/',views.editjob,name='editjob'),
    path('editintern/<int:id>/', views.editintern, name='editintern'),
    path('previewjob/<int:id>/',views.previewjob,name='previewjob'),
    # path('previewintern/<int:id>/',views.previewintern,name='previewintern'),
    path('jobdetails/<int:id>/',views.jobdetails,name='jobdetails'),


    path('editprofile/<int:id>/',views.editemployeerprofile,name='editemployeerprofile'),
    path('profileverify/',views.profileverify,name='profileverify'),
    path('payment/',views.payment,name='payment'),
    path('paymentintern/',views.paymentintern,name='paymentintern'),
    path('paymenthandler/', views.paymenthandler, name='paymenthandler'),
    path('internhandler/', views.internhandler, name='internhandler'),
    path('employeer/alljobapplicants/',views.alljobapplicants,name='alljobapplicants'),
    path('employeer/applicantdetails/<int:id>/<int:id2>',views.applicantdetails,name='applicantdetails'),
    path('add/showpdf/<int:id>/',views.showpdf,name='showpdf'),

    path('alljobsposted/',views.alljobsposted,name='alljobsposted'),
    path('specificapplicant/<int:id>/',views.specificapplicant,name='specificapplicant'),
    path('addscheduleinterview/', views.addscheduleinterview, name='addscheduleinterview'),
    path('rescheduleinterview/<int:interview_id>/', views.rescheduleinterview, name='rescheduleinterview'),
    path('addmeetinglink/', views.addmeetinglink, name='addmeetinglink'),
    



    
#Moderator Page URLS

    path('employerslist', views.employerslist, name='employerslist'),
    path('jobseekerslist', views.jobseekerslist, name='jobseekerslist'),
    path('employerdetails/<int:id>/', views.employerdetails, name='employerdetails'),
    path('accept/<int:id>/', views.accept, name='accept'),
    path('reject/<int:id>/', views.reject, name='reject'),


#Jobseeker Page Urls
    path('editprofile', views.editprofile, name='editprofile'),
    # path('editresume', views.editresume, name='editresume'),
    path('editresume/<int:id>/', views.editresume, name='editresume'),
    path('joblisting/', views.joblisting, name='joblisting'),
    path('generate-pdf-report/', generate_pdf_report, name='generate_pdf_report'),
    path('jobdetails/<int:id>', views.jobsindetail, name='jobsindetail'),
    path('appliedjobs', views.appliedjobs, name='appliedjobs'),
    path('eligibility', views.eligibility, name='eligibility'),
    path('appliedjobstatus/<int:id>/', views.appliedjobstatus, name='appliedjobstatus'),
    
    path('reset_password/',auth_views.PasswordResetView.as_view(),name="reset_password"),     
    path('reset_password_sent/',auth_views.PasswordResetDoneView.as_view(),name="password_reset_done"),     
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(),name="password_reset_confirm"),     
    path('reset_password_complete/',auth_views.PasswordResetCompleteView.as_view(),name="password_reset_complete"), 
    path('notifications/',views.notifications,name='notifications'),
    path('resume', views.resume, name='resume'),
    path('resumelist', views.resumelist, name='resumelist'),
    path('thankyou', views.thankyou, name='thankyou'),
    path('resumebldrhomepage', views.resumebldrhomepage, name='resumebldrhomepage'),
    path('feedbacks', views.feedbacks, name='feedbacks'),
    path('my_form', views.my_form, name='my_form'),
    path('my_post', views.my_post, name='my_post'),
    path('postintern', views.postintern, name='postintern'),
    path('premiumservices', views.premiumservices, name='premiumservices'),
    path('resumebuilderform/', views.resumebuilderform, name='resumebuilderform'),
    path('resumepreview/<int:id>/', views.resumepreview, name='resumepreview'),
    path('notifications/',views.notifications,name='notifications'),
    path('userpaymentdetails/', views.userpaymentdetails, name='userpaymentdetails'),
    path('manageintern/<int:id>/', views.manageintern, name='manageintern'),
    path('intern', views.intern, name='intern'),
    path('interneligibility', views.interneligibility, name='interneligibility'),
    path('interndetails/<int:id>/',views.interndetails,name='interndetails'),

     ]
 