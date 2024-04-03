from django.shortcuts import render,redirect,HttpResponse
# from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from app1.models import Jobseeker,Employeer,User,EmployeerProfile,Verificationdetails,JobseekerProfile
from app1.models import candidateSkillsandTechnologies,JobapplicationDetails,Interviewscheduling,ResumeSchema,PayementDetails
from .models import Interviewscheduling
from django.contrib import messages
import json
# from .models import internship
# from .models import classdetails
from app1.models import Jobdetails,User
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .forms import ProfileForm
from .models import feedback
from django.shortcuts import render
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest
from collections import Counter
from django.conf import settings
from django.http import HttpResponse, Http404
import os
from django.db.models import Q
import PyPDF2
import openai
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

from skillNer.general_params import SKILL_DB
import os
from twilio.rest import Client


def index(request):
    return render(request,"home.html")

def loginpage(request):
    # if request.user.is_authenticated:
    #     return redirect('loginpage')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user=authenticate(request,username=username,password=password)

        if user is not None and user.role == 'EMPLOYEER':
            login(request, user)
            return redirect('employeerpage')
        elif user is not None and user.role == 'JOBSEEKER':
            login(request, user)
            return redirect('candidatepage') 
        elif user is not None and user.role == 'MODERATOR':
            login(request, user)
            return redirect('adminpage') 
        else:
             messages.error(request,"Invalid Credentials" )
             return redirect('loginpage')
    else:
        msg = 'error validating form'
    return render(request,'login.html')
       


def check_username(request):
    User = get_user_model()
    if request.method == 'POST':
        username = request.POST.get('username')
        # Check if the username is available in the database
        if User.objects.filter(username=username).exists():
            # Return 'not available' if the username already exists in the database
            return JsonResponse({'status': 'not available'})
        else:
            # Return 'available' if the username is available
            return JsonResponse({'status': 'available'})

def check_email(request):
    User = get_user_model()
    if request.method == 'POST':
        email = request.POST.get('email')
        # Check if the email is available in the database
        if User.objects.filter(email=email).exists():
            # Return 'not available' if the email already exists in the database
            return JsonResponse({'status': 'not available'})
        else:
            # Return 'available' if the email is available
            return JsonResponse({'status': 'available'})

def jsregpage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        cpassword = request.POST.get('cpassword')
        if password == cpassword:
            js_user = Jobseeker.objects.create_user(
                username = username,
                email=email,
                password=password,
                )
            js_user.save()
            return redirect('loginpage')
      

       
    return render(request,"jsregistartion.html")

def rregpage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        cpassword = request.POST.get('cpassword')
        if password == cpassword:
            r_user = Employeer.objects.create_user(
                username = username,
                email=email,
                password=password,

                )
            r_user.save()
            return redirect('loginpage')

    return render(request,"rregistration.html")

def logout_view(request):
    logout(request)
    return redirect('loginpage')

#Employeer Views 
@login_required(login_url='/login')
def postjob(request):
    userid = request.user.id
    vdetails = Verificationdetails.objects.get(user_id=userid)
    value = vdetails.isverified

    if request.method == 'POST':
        jobtitle = request.POST.get('job_title')
        jobdescription = request.POST.get('job_description')
        email = request.POST.get('contact_email')
        jobtype = request.POST.get('jobtype')
        experience = request.POST.get('experience')
        vaccancies = request.POST.get('vaccancies')
        lastdate = request.POST.get('lastdate')
        office_location = request.POST.get('office_location')
  # Retrieve office location

        postedjob = Jobdetails(
            job_title=jobtitle,
            job_description=jobdescription,
            contact_email=email,
            job_type=jobtype,
            experience=experience,
            vacancies=vaccancies,
            lastdate=lastdate,
            office_location=office_location  # Save office location
        )
        postedjob.cmp_id = request.user
        postedjob.save()

        messages.success(request, "Job is Successfully Posted")
        return redirect(reverse('managejobs', args=[userid]))
    else:
        current_value = request.user
        user_id = current_value.id
        context = {
            'user_id': user_id,
            'verified': value,
        }
        return render(request, 'employeer/postjob.html', context)





# Job Post Seeting and Add Qualification

# def addqualification(request,id):
#     if request.user.is_authenticated:
#         userid=request.user.id
#         vdetails = Verificationdetails.objects.get(user_id=userid)
#         value=vdetails.isverified

#         if request.method == 'POST':
#             quali =request.POST.get('qualification')

#             addedqualification= Qualifications(
#                 qualification_name=quali,
#                 )
#             addedqualification.cmp_id=request.user
#             addedqualification.save()
#             messages.success(request,"Qualification is added" )
#             return redirect(request.META['HTTP_REFERER'])
        
        
#         pos = Qualifications.objects.filter(cmp_id_id=id)
#         context ={
#             'pos': pos,
#             'value':value,
#         }
#         return render(request,'employeer/addqualification.html',context)
#     return redirect('loginpage')

# def qualificationdelete(request,id):
#         quali = Qualifications.objects.filter(quali_id=id)
#         quali.delete()
#         return redirect(request.META.get('HTTP_REFERER'))

# @login_required(login_url='/login')
# def qualificationupdate(request,id):
#     quali = Qualifications.objects.get(pk=id)
#     if request.method == 'POST':
#         value =request.POST.get('qualification')
#         Qualifications.objects.filter(quali_id=id).update(qualification_name=value)
#         value = quali.cmp_id_id
#         return redirect(reverse('addqualification',args=[value]))
#     else:   
             
#         current_value = quali.qualification_name
#         return render(request,'employeer/editqualification.html',{
#             'detail':quali,'current_value':current_value
#     })

# Manage job ,Delete Job ,Update Job


def deletejob(request,id):
        jobs = Jobdetails.objects.filter(job_id=id)
        jobs.delete()
        return redirect(request.META.get('HTTP_REFERER'))
def deleteintern(request,id):
        interns = interndetails.objects.filter(job_id=id)
        interns.delete()
        return redirect(request.META.get('HTTP_REFERER'))

def eligibility(request):
    return render(request,"eligibility.html")

def interneligibility(request):
    return render(request,"interneligibility.html")


# Job  Setting and Add Skills

# def addskills(request,id):
#     if request.user.is_authenticated:
#         userid=request.user.id
#         vdetails = Verificationdetails.objects.get(user_id=userid)
#         value=vdetails.isverified

#         if request.method == 'POST':
#             skill =request.POST.get('skills')
#             value =EmployeerProfile.objects.get(user_id=userid)
#             addedskills= Skills(
#                 skill_name=skill
#                 )
#             addedskills.emp_profile_id=userid
#             addedskills.save()
#             messages.success(request,"Skill is added" )
#             return redirect(request.META['HTTP_REFERER'])
        
        
#         pos = Skills.objects.filter(emp_profile_id=id)
#         context ={
#             'pos': pos,
#             'value':value,
#         }
#         return render(request,'employeer/addskill.html',context)
#     return redirect('loginpage')

# def skilldelete(request,id):
#         skill = Skills.objects.filter(skill_id=id)
#         skill.delete()
#         return redirect(request.META.get('HTTP_REFERER'))

# @login_required(login_url='/login')
# def skillupdate(request,id):
#     skill = Skills.objects.get(pk=id)
#     if request.method == 'POST':
#         value =request.POST.get('skills')
#         Skills.objects.filter(skill_id=id).update(skill_name=value)
#         value =skill.emp_profile_id
#         return redirect(reverse('addskills',args=[value]))
#     else:   
             
#         current_value = skill.skill_name
#         return render(request,'employeer/editskill.html',{
#             'detail':skill,'current_value':current_value
#     })









def managejobs(request ,id):
    if request.user.is_authenticated:
        pos = Jobdetails.objects.filter(cmp_id_id=id)
        if request.method =='POST':
            searched = request.POST['searched']
            jobs=Jobdetails.objects.filter(job_title__contains=searched)
            context={
                'searched':searched,
                'jobs':jobs,
            }
            return render(request,'employeer/managejobs.html',context) 
        
        else:
            context ={
                'pos': pos,
                'id':id
            }
            return render(request,'employeer/managejobs.html',context) 
    return redirect('loginpage')





@login_required(login_url='/login')

def editjob(request,id):
    jb = Jobdetails.objects.get(pk=id)
    idvalue= request.user
    # allqualifications = Qualifications.objects.filter(cmp_id_id=idvalue)
    if request.method == 'POST':
        jobtitle= request.POST.get('job_title')
        jobdescription = request.POST.get('job_description')
        email = request.POST.get('contact_email')
        jobtype = request.POST.get('jobtype')
        # specialisation= request.POST.get('specialisation')
        experience = request.POST.get('experience')
        # salary = request.POST.get('salary')
        vaccancies = request.POST.get('vaccancies')
        # qualification=request.POST.get('qualification')
        lastdate = request.POST.get('lastdate')
        Jobdetails.objects.filter(job_id=id).update(
            job_title=jobtitle,
            job_description=jobdescription,
            contact_email=email,
            job_type=jobtype,
            # specialisation=specialisation,
            # experience=experience,
            # expected_salary=salary,
            vacancies=vaccancies,
            # qualification=qualification,
            lastdate=lastdate,)
        value = jb.cmp_id_id
        return redirect(reverse('managejobs',args=[value]))
    else:  

        jobtitle = jb.job_title
        jobdescription = jb.job_description
        email = jb.contact_email
        jobtype = jb.job_type
        # specialisation=jb.specialisation
        experience=jb.experience
        # salary=jb.expected_salary
        vaccancies=jb.vacancies
        # qualification=jb.qualification
        lastdate=jb.lastdate

        context={
            'detail':jb,
            'jobtitle': jobtitle,
            'jobdescription':jobdescription,
            'email':email,
            'jobtype':jobtype,
            # 'specialisation':specialisation,
            'experience':experience,
            # 'salary':salary,
            'vaccancies':vaccancies,
            # 'qualification':qualification,
            'lastdate':lastdate,
            # 'qualificationdetails':allqualifications
        }
        return render(request,'employeer/editjob.html',context)

from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .models import ResumeSchema

def editresume(request, id):
    resume_detail = get_object_or_404(ResumeSchema, pk=id)
    
    if request.method == 'POST':
        resumetitle = request.POST.get('resumetitle')
        name = request.POST.get('name')
        careerobjective = request.POST.get('careerobjective')
        address = request.POST.get('address')
        phonenumber = request.POST.get('phonenumber')
        email = request.POST.get('email')
        skills = request.POST.get('skills')
        projecttitle = request.POST.get('projecttitle')
        projectdescription = request.POST.get('projectdescription')
        profilepic = request.FILES.get('profilepic')
        collegename = request.POST.get('collegename')
        coursename = request.POST.get('coursename')
        passingyear = request.POST.get('passingyear')
        hssname = request.POST.get('hssname')
        hssyear = request.POST.get('hssyear')
        hssmarks = request.POST.get('hssmarks')
        tenthschoolname = request.POST.get('tenthschoolname')
        tenthpassyear = request.POST.get('tenthpassyear')
        tenthmarks = request.POST.get('tenthmarks')

        # Update the resume details
        resume_detail.resumetitle = resumetitle
        resume_detail.seekername = name
        resume_detail.careerobjective = careerobjective
        resume_detail.address = address
        resume_detail.phonenumber = phonenumber
        resume_detail.email = email
        resume_detail.skills = skills
        resume_detail.projecttitle = projecttitle
        resume_detail.projectdescription = projectdescription
        resume_detail.profilepicture = profilepic
        resume_detail.collegename = collegename
        resume_detail.coursename = coursename
        resume_detail.passingyear = passingyear
        resume_detail.hssname = hssname
        resume_detail.hssyear = hssyear
        resume_detail.hssmarks = hssmarks
        resume_detail.tenthschoolname = tenthschoolname
        resume_detail.tenthpassyear = tenthpassyear
        resume_detail.tenthmarks = tenthmarks
        resume_detail.save()

        return redirect(reverse('resumepreview', args=[resume_detail.resume_id]))
    
    else:
        context = {
            'detail': resume_detail,
        }
        return render(request, 'resumebuilderform.html', context)



# Change Status
# def changestatus(request,id):
#     quali = Qualifications.objects.get(quali_id=id)
#     status_value = quali.status
#     if status_value == 0:
#         quali.status=1
#         quali.save()
#     else:
#         quali.status=0
#         quali.save()
        
#     return redirect(request.META.get('HTTP_REFERER'))


# def changeskillstatus(request,id):
#     skill = Skills.objects.get(skill_id=id)
#     status_value = skill.status
#     if status_value == 0:
#         skill.status=1
#         skill.save()
#     else:
#         skill.status=0
#         skill.save()
        
#     return redirect(request.META.get('HTTP_REFERER'))

   


# class QualificationDelete(generic.DeleteView):
#     model=Qualifications
#     template_name= 'addqualifications.html'
#     success_url=reverse_lazy('employeer/addqualifications/<int:id>')
def editemployeerprofile(request,id):
    if request.user.is_authenticated:
        details = EmployeerProfile.objects.get(user_id=id)
        if request.method == 'POST':
            company_name= request.POST.get('Company-Name')
            office_location = request.POST.get('Office-Location')
            address = request.POST.get('Address')
            phone_number = request.POST.get('Phoneno')
            company_logo = request.FILES.get('logo')
            EmployeerProfile.objects.filter(user_id=id).update(
            company_name = company_name,
            office_location = office_location,
            address = address,
            phone_number = phone_number,
            )
            if details.company_logo and company_logo:
                    details.company_logo.delete()
            if company_logo:
                details.company_logo = company_logo
                details.save()

            return redirect('employeerpage')
        else: 
            company_name= details.company_name
            office_location = details.office_location
            address = details.address
            phone_number = details.phone_number
            company_logo= details.company_logo
            context={
                "company_name":company_name,
                "office_location":office_location,
                "address":address,
                "phone_number":phone_number,
                "company_logo":company_logo,
            }
            return render(request,'employeer/editprofile.html',context)

    return redirect('loginpage')





def previewjob(request,id):
    if request.user.is_authenticated:
      jobdetails = Jobdetails.objects.get(job_id=id)  
      userid = request.user 
      details= EmployeerProfile.objects.get(user_id=userid)

      jobtitle=jobdetails.job_title
      clogo = details.company_logo
      type= jobdetails.job_type
      jobid = jobdetails.job_id
      context={
          "job_title":jobtitle,
          "c_logo":clogo,
          "type":type,
          "id":jobid,
      }


      return render(request,'employeer/jobpreview.html',context)

    return redirect('loginpage')

# def previewintern(request,id):
#     if request.user.is_authenticated:
#       interndetails = interndetails.objects.get(job_id=id)  
#       userid = request.user 
#       details= EmployeerProfile.objects.get(user_id=userid)

#       interntitle=interndetails.title
#     #   clogo = details.company_logo
#       mode= interndetails.mode
#       jobid = interndetails.job_id
#       context={
#           "intern_title":interntitle,
#         #   "c_logo":clogo,
#           "mode":mode,
#           "id":jobid,
#       }


#       return render(request,'employeer/jobpreview.html',context)

#     return redirect('loginpage')


def jobdetails(request,id):
    if request.user.is_authenticated:

        jobdetails = Jobdetails.objects.get(job_id=id)  
        userid = request.user 
        details= EmployeerProfile.objects.get(user_id=userid)
        jobtitle=jobdetails.job_title
        clogo = details.company_logo
        type= jobdetails.job_type
        description = jobdetails.job_description
        lastdate=jobdetails.lastdate
        location = details.office_location
        experience= jobdetails.experience
        vaccancies = jobdetails.vacancies
       
        context={
            "job_title":jobtitle,
            "c_logo":clogo,
            "type":type,
            "description":description,
            "lastdate":lastdate,
            "location":location,
            "experience":experience,
            "vaccancies":vaccancies,
        }



        return render(request,'employeer/jobpreviewdetail.html',context)
    return redirect('loginpage')

def profileverify(request):
     if request.user.is_authenticated:
        if request.method == 'POST':
            userid=request.user.id  
            # # all=Verificationdetails.objects.all()
            # # for i in all:
            # #  if userid == i.user_id:
            # #     messages.warning(request,"Verification Details is Already Added" )
            #     return redirect(request.META['HTTP_REFERER'])
            bc=Verificationdetails.objects.get(user_id=userid)
            buisness_license = request.FILES.get('buisness-license')
            # prooftype = request.POST.get('recruiter-id')
            # proof = request.FILES.get('fileupload')

            if bc.buisnesslicence and buisness_license:
                bc.buisnesslicence.delete()
            if buisness_license:
                bc.buisnesslicence = buisness_license
                bc.save()


            # if bc.proof and proof:
            #     bc.proof.delete()
            # if proof:
            #     bc.proof = proof
            #     bc.save()
           
            
            return redirect('employeerpage')
             
        else:
            return render(request,'employeer/verifyprofile.html')
     return redirect('loginpage')


def alljobapplicants(request):
    if request.user.is_authenticated:
        
        user_id=request.user.id
        emp_profile_details=EmployeerProfile.objects.get(user_id=user_id)
        emp_profile_id=emp_profile_details.id

        applicationdetails=JobapplicationDetails.objects.filter(employerprofile_id=emp_profile_id)
        jobdetails=Jobdetails.objects.all()
        profiledetails=JobseekerProfile.objects.all()
        context={

            "applicationdetails":applicationdetails,
            "jobdetails":jobdetails,
            "profiledetails":profiledetails,
        }
        return render(request, 'employeer/alljobapplicants.html',context)
    return redirect('loginpage')

def applicantdetails(request,id,id2):
    if request.user.is_authenticated:
        profiledetails=JobseekerProfile.objects.get(id=id)
        applicationdetails=JobapplicationDetails.objects.get(application_id=id2)
        jobdetails=Jobdetails.objects.all()
        image_path = os.path.join(settings.MEDIA_ROOT, profiledetails.profile_photo.name)
        scheduledetails=Interviewscheduling.objects.filter(application_id=id2)
        context={
            "profilelogo":profiledetails.profile_photo,
            "profileid":id,
            "firstname":profiledetails.first_name,
            "lastname":profiledetails.last_name,
            "email":profiledetails.email,
            "phone":profiledetails.phone_number,
            "age":profiledetails.age,
            "qualification":profiledetails.highestqualification,
            "fulladdress":profiledetails.fulladdress,
            # "resume":resume_pdf,
            "applictiondetails":applicationdetails,
            "jobdetails":jobdetails,
            "jobid": applicationdetails.job_id,
            "appid":applicationdetails.application_id,
            "scheduledetails":scheduledetails,
          
        }
        return render(request, 'employeer/applicantdetails.html',context)
    return redirect('loginpage')

# def chatbox(request,id):
#     if request.user.is_authenticated:
#         userid=request.user.id
#         empprofile=EmployeerProfile.objects.get(user_id=userid)
#         profiledetails=JobseekerProfile.objects.get(id=id)
#         context={
#             "profilelogo":profiledetails.profile_photo,
#             "profileid":id,
#             "firstname":profiledetails.first_name,
#             "lastname":profiledetails.last_name,
#             "loggeduserid":userid,
#             "senttouserid":profiledetails.user_id,
#             "empprofiledetails":empprofile,

#         }

#         return render(request, 'employeer/chatbox.html',context)
#     return redirect('loginpage')




def showpdf(request, id):
    applicationdetails = JobapplicationDetails.objects.get(application_id=id)
    pdf_path = os.path.join(settings.MEDIA_ROOT, applicationdetails.applicant_resume.name)
        
    with open(pdf_path, 'rb') as pdf_file:
        resume_pdf = HttpResponse(pdf_file.read(), content_type='application/pdf')
        resume_pdf['Content-Disposition'] = f'filename="{applicationdetails.applicant_resume.name}"'
    
    return resume_pdf

def alljobsposted(request):
    if request.user.is_authenticated:

        userdetails =request.user.id;
        jobdetails = Jobdetails.objects.filter(cmp_id_id=userdetails)
        # sample=[jobdetails.job_id,]
        sample = []
        for jobdetail in jobdetails:
            sample.append(jobdetail.job_id)

        empprofileid = EmployeerProfile.objects.get(user_id=userdetails)
        allapplicants =JobapplicationDetails.objects.filter(employerprofile_id=empprofileid).values_list("job_id",flat=True)
        # counts=dict(Counter(allapplicants))
        #print(type(counts))
        counts={'a':1,'b':2}
       
        context={
            "jobdetails":jobdetails,
            "counts":counts,
           
        }
        return render(request,"employeer/alljobsposted.html",context)
    return redirect('loginpage')



# def specificapplicant(request, id):
#     if request.user.is_authenticated:
#         empid = request.user.id
#         empprofile = EmployeerProfile.objects.get(user_id=empid)
#         applicationdetails = JobapplicationDetails.objects.filter(job_id=id, employerprofile_id=empprofile.id)
#         jobdetails = Jobdetails.objects.get(job_id=id)
        
#         if applicationdetails.exists():
#             applicants = []

#             for application in applicationdetails:
#                 jobseeker_id = application.jobseekerprofile_id
#                 applicant_resume = application.applicant_resume.path

#                 with open(applicant_resume, 'rb') as filehandle:
#                     pdfReader = PyPDF2.PdfReader(filehandle)
#                     pagehandle = pdfReader.pages[0]
#                     text = pagehandle.extract_text()
#                     text = text.replace('o', '')
#                     text = text.replace('|', '')
#                     print(text)

#                     similarity_score = 0.0  # Initialize similarity score as 0

#                     # Calculate similarity score if needed
#                     # Place your similarity calculation logic here

#                 applicants.append({
#                     'jobseeker_id': jobseeker_id,
#                     'resume_text': text,
#                     'application_id': application.application_id,
#                     'similarity_score': similarity_score,
#                 })

#             # Sort applicants by similarity score (you can modify this as needed)
#             sorted_applicants = sorted(applicants, key=lambda x: x['similarity_score'], reverse=True)

#             print(sorted_applicants)
        
#         jobseeker = JobseekerProfile.objects.all()

#         context = {
#             "applicantdetails": applicationdetails,
#             "jobdetails": jobdetails,
#             "employerprofile": empprofile,
#             "jobseeker": jobseeker,
#             "sorted_applicants": sorted_applicants,
#         }

#         return render(request, "employeer/specificapplicant.html", context)
#     else:
#         return redirect('loginpage')

from django.shortcuts import render, redirect
from .models import JobapplicationDetails, Jobdetails, EmployeerProfile, JobseekerProfile

from django.shortcuts import render, redirect
from .models import JobapplicationDetails, Jobdetails, EmployeerProfile, JobseekerProfile

def specificapplicant(request, id):
    if request.user.is_authenticated:
        empid = request.user.id
        empprofile = EmployeerProfile.objects.get(user_id=empid)
        applicationdetails = JobapplicationDetails.objects.filter(job_id=id, employerprofile_id=empprofile.id)
        jobdetails = Jobdetails.objects.get(job_id=id)
        
        if applicationdetails.exists():
            applicants = []

            for application in applicationdetails:
                jobseeker_id = application.jobseekerprofile_id

                # Fetch experience for the current jobseeker
                jobseeker_experience = JobseekerProfile.objects.get(id=jobseeker_id).experience
                
                # Fetch CGPA for the current jobseeker
                jobseeker_cgpa = JobseekerProfile.objects.get(id=jobseeker_id).cgpa
                
                # Fetch skills for the current jobseeker
                jobseeker_skills = JobseekerProfile.objects.get(id=jobseeker_id).skills
                
                applicants.append({
                    'jobseeker_id': jobseeker_id,
                    'jobseeker_name': JobseekerProfile.objects.get(id=jobseeker_id).first_name + " " + JobseekerProfile.objects.get(id=jobseeker_id).last_name,
                    'profile_photo': JobseekerProfile.objects.get(id=jobseeker_id).profile_photo.url,
                    'application_id': application.application_id,
                    'experience': jobseeker_experience,
                    'cgpa': jobseeker_cgpa,
                    'skills': jobseeker_skills,
                })

            # Apply filtering based on user input
            cgpa_filter = request.GET.get('cgpa')
            experience_filter = request.GET.get('experience')
            skill_filter = request.GET.get('skill')

            if cgpa_filter:
                applicants = [applicant for applicant in applicants if applicant['cgpa'] == cgpa_filter]
            if experience_filter:
                applicants = [applicant for applicant in applicants if applicant['experience'] == experience_filter]
            if skill_filter:
                applicants = [applicant for applicant in applicants if skill_filter in applicant['skills']]

        jobseeker = JobseekerProfile.objects.all()

        context = {
            "applicantdetails": applicationdetails,
            "jobdetails": jobdetails,
            "employerprofile": empprofile,
            "jobseeker": jobseeker,
            "sorted_applicants": applicants,
        }

        return render(request, "employeer/specificapplicant.html", context)
    else:
        return redirect('loginpage')



def addscheduleinterview(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        duration = data.get('duration')
        interviewtype = data.get('interviewType')
        timeanddate = data.get('timeAndDate')
        applicationid = data.get('applicationId')
        jobid = data.get('jobid')
        existing_interview = Interviewscheduling.objects.filter(
            application_id=applicationid,
            interview_timeanddate=timeanddate
        ).exists()
        if existing_interview:
            return JsonResponse({'status': 'Interview already scheduled for this application'})
        try:
            interviewdetails = Interviewscheduling(
                time_duration=duration,
                interview_type=interviewtype,
                interview_timeanddate=timeanddate,
                application_id=applicationid,
                job_id=jobid,
            )
            interviewdetails.save()
            account_sid = "ACd7f9a7af932c77e184595c03e35117d9"
            auth_token = "c493f7344688d2e1f93b37127a265126"
            client = Client(account_sid, auth_token)
            message = client.messages.create(
            body="Your Interview has been Scheduluded please check the hireu web portal",
            from_="+16205165561",
            to="+919744608229"
            )
            print(message.sid)
            return JsonResponse({'status': 'Success'})
        except:
            return JsonResponse({'status': 'Invalid'})
    else:
        return HttpResponse("Invalid request method")




def rescheduleinterview(request,id):
   
    if request.method == 'POST':
        duration = request.POST.get('duration')
        interviewtype = request.POST.get('interviewtype')
        timeanddate = request.POST.get('timeanddate')
        Interviewscheduling.objects.filter(interview_id=id).update(
            time_duration=duration,
            interview_type=interviewtype,
            interview_timeanddate=timeanddate,
            )
    else:
        interviewscheduling=Interviewscheduling.objects.get(interview_id=id)
        context={
            "timeduration":interviewscheduling.time_duration,
            "interviewtype":interviewscheduling.interview_type,
            "timeanddate":interviewscheduling.interview_timeanddate,
        }
    return JsonResponse(context)


def addmeetinglink(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        meetinglink = data.get('meetinglink')
        interviewid=data.get('interviewid')
        existing_interview = Interviewscheduling.objects.filter(
           interview_id=interviewid,
           interviewlink=meetinglink,
        ).exists()
        if existing_interview:
            return JsonResponse({'status': 'Meeting  Link is already added'})
        try:
            Interviewscheduling.objects.filter(interview_id=interviewid).update(
            interviewlink=meetinglink
            )
            return JsonResponse({'status': 'Success'})
        except:
            return JsonResponse({'status': 'Invalid'})
    else:
        return HttpResponse("Invalid request method")


   








# Jobseeker Views

@login_required(login_url='/login')
def candidatepage(request):
    if request.user.is_authenticated:
        return render(request,'jobseeker/home.html')
    return redirect('loginpage')

# def joblisting(request):

#     userid=request.user.id
#     jobseekerprofile=JobseekerProfile.objects.get(user_id=userid)
#     profile_id=jobseekerprofile.id  
#     jobseekerskills = candidateSkillsandTechnologies.objects.get(id=profile_id)
#     jobseeker_skills =jobseekerskills.skill_name
#     jobseeker_skill_list=[s.strip() for s in jobseeker_skills.split(',')] 
#     if request.user.is_authenticated:
#         if request.method =='POST':
#             searched = request.POST['searched']
#             jobs=Jobdetails.objects.filter(job_title__contains=searched)
#             profiledetails=EmployeerProfile.objects.all()
#             context={
#                 'searched':searched,
#                 'jobs':jobs,
#                 'profiledetails':profiledetails,
#             }
#             return render(request,'jobseeker/jobs.html',context) 
#         else:
#             allspecialisations = Jobdetails.objects.values_list('specialisation', flat=True)
#             matching_skills = []

#             skills = Skills.objects.all()
#             for skill in skills:
#                 for specialisation in allspecialisations:
#                     if skill.skill_id == specialisation:
#                         matching_skills.append(skill.skill_name)

#             jobdetails = Jobdetails.objects.all()
#             profiledetails=EmployeerProfile.objects.all()
#             context={
#                     "jobdetails":jobdetails,
#                     "profiledetails":profiledetails,
#             }



          
#             return render(request,'jobseeker/jobs.html',context)

            
#     return redirect('loginpage')
"""
def joblisting(request):
    if request.user.is_authenticated:
        

        userid = request.user.id
        jobseekerprofile = JobseekerProfile.objects.get(user_id=userid)
        profile_id = jobseekerprofile.id  

        try:
            jobseekerskills = candidateSkillsandTechnologies.objects.get(id=profile_id)
            jobseeker_skills = jobseekerskills.skill_name
            jobseeker_skill_list = [s.strip() for s in jobseeker_skills.split(',')]
        except candidateSkillsandTechnologies.DoesNotExist:
            jobseeker_skill_list = []

        # jobseekerskills = candidateSkillsandTechnologies.objects.get(id=profile_id)
        # jobseeker_skills = jobseekerskills.skill_name
        # jobseeker_skill_list = [s.strip() for s in jobseeker_skills.split(',')] 

        if request.method == 'POST':
            searched = request.POST['searched']
            jobs = Jobdetails.objects.filter(job_title__contains=searched)
            profiledetails = EmployeerProfile.objects.all()
            context = {
                'searched': searched,
                'jobs': jobs,
                'profiledetails': profiledetails,
            }
            return render(request, 'jobseeker/jobs.html', context) 
        else:
            job_details_dict = {}
            jobdetails=Jobdetails.objects.all()
           

            for job in jobdetails:
                job_skills = [s.strip() for s in job.specialisation.split(',')]
                matching_skills = set(job_skills) & set(jobseeker_skill_list)
                matching_score = len(matching_skills) / len(job_skills) * 100 if job_skills else 0
                job_details_dict[job] = matching_score
            sorted_job_details = sorted(job_details_dict.items(), key=lambda x: x[1], reverse=True)
            sorted_jobs = [job for job, _ in sorted_job_details]

            p = Paginator(sorted_jobs,4)
            page=request.GET.get('page')
            jos=p.get_page(page)

            profiledetails = EmployeerProfile.objects.all()
            context = {
                'jobdetails': jos,
                'profiledetails': profiledetails,
                'pages':jos
            }
            return render(request, 'jobseeker/jobs.html', context)
    else:
        return redirect('loginpage')
"""


from django.db.models import Q
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.utils import timezone
from .models import Jobdetails, JobseekerProfile, EmployeerProfile, JobapplicationDetails

def joblisting(request):
    if request.user.is_authenticated:
        userid = request.user.id
        jobseekerprofile = JobseekerProfile.objects.get(user_id=userid)
        profile_id = jobseekerprofile.id  

        try:
            jobseekerskills = candidateSkillsandTechnologies.objects.get(id=profile_id)
            jobseeker_skills = jobseekerskills.skill_name
            jobseeker_skill_list = [s.strip() for s in jobseeker_skills.split(',')]
        except candidateSkillsandTechnologies.DoesNotExist:
            jobseeker_skill_list = []

        if request.method == 'POST':
            searched = request.POST.get('searched')
            location_searched = request.POST.get('location_searched')

            # Filter jobs based on search query and/or location
            jobs_query = Q()
            if searched:
                jobs_query |= Q(job_title__icontains=searched)
            if location_searched:
                jobs_query |= Q(office_location__icontains=location_searched)

            jobs = Jobdetails.objects.filter(jobs_query)
            profiledetails = EmployeerProfile.objects.all()

            # Check if the last date has passed for each job in the search results
            for job in jobs:
                if job.lastdate < timezone.now().date():
                    job.is_last_date_passed = True
                else:
                    job.is_last_date_passed = False

            context = {
                'searched': searched,
                'location_searched': location_searched,
                'jobs': jobs,
                'profiledetails': profiledetails,
            }
            return render(request, 'jobseeker/jobs.html', context) 
        else:
            applied_jobs = JobapplicationDetails.objects.filter(jobseekerprofile=jobseekerprofile).values_list('job_id', flat=True)
            jobdetails = Jobdetails.objects.exclude(job_id__in=applied_jobs)

            # Check if the last date has passed for each job in the main job listing
            for job in jobdetails:
                if job.lastdate < timezone.now().date():
                    job.is_last_date_passed = True
                else:
                    job.is_last_date_passed = False

            job_details_dict = {}
            for job in jobdetails:
                job_skills = [s.strip() for s in job.specialisation.split(',')]
                matching_skills = set(job_skills) & set(jobseeker_skill_list)
                matching_score = len(matching_skills) / len(job_skills) * 100 if job_skills else 0
                job_details_dict[job] = matching_score
            sorted_job_details = sorted(job_details_dict.items(), key=lambda x: x[1], reverse=True)
            sorted_jobs = [job for job, _ in sorted_job_details]

            p = Paginator(sorted_jobs, 4)
            page = request.GET.get('page')
            jos = p.get_page(page)

            profiledetails = EmployeerProfile.objects.all()
            context = {
                'jobdetails': jos,
                'profiledetails': profiledetails,
                'pages': jos
            }
            return render(request, 'jobseeker/jobs.html', context)
    else:
        return redirect('loginpage')









def internlisting(request):
    if request.user.is_authenticated:
        userid = request.user.id
        jobseekerprofile = JobseekerProfile.objects.get(user_id=userid)
        profile_id = jobseekerprofile.id  

        try:
            jobseekerskills = candidateSkillsandTechnologies.objects.get(id=profile_id)
            jobseeker_skills = jobseekerskills.skill_name
            jobseeker_skill_list = [s.strip() for s in jobseeker_skills.split(',')]
        except candidateSkillsandTechnologies.DoesNotExist:
            jobseeker_skill_list = []

        if request.method == 'POST':
            searched = request.POST['searched']
            jobs = interndetails.objects.filter(job_title__contains=searched)
            profiledetails = EmployeerProfile.objects.all()
            context = {
                'searched': searched,
                'jobs': jobs,
                'profiledetails': profiledetails,
            }
            return render(request, 'intern.html', context) 
        else:
            applied_jobs = JobapplicationDetails.objects.filter(jobseekerprofile=jobseekerprofile).values_list('job_id', flat=True)
            jobdetails = interndetails.objects.exclude(job_id__in=applied_jobs)

            job_details_dict = {}
            for job in jobdetails:
                job_skills = [s.strip() for s in job.specialisation.split(',')]
                matching_skills = set(job_skills) & set(jobseeker_skill_list)
                matching_score = len(matching_skills) / len(job_skills) * 100 if job_skills else 0
                job_details_dict[job] = matching_score
            sorted_job_details = sorted(job_details_dict.items(), key=lambda x: x[1], reverse=True)
            sorted_jobs = [job for job, _ in sorted_job_details]

            p = Paginator(sorted_jobs,4)
            page=request.GET.get('page')
            jos=p.get_page(page)

            profiledetails = EmployeerProfile.objects.all()
            context = {
                'jobdetails': jos,
                'profiledetails': profiledetails,
                'pages':jos
            }
            return render(request, 'intern.html', context)
    else:
        return redirect('loginpage')
















def jobsindetail(request,id):
    if request.user.is_authenticated:
        userid= request.user.id
        jobseekerprofie=JobseekerProfile.objects.get(user_id=userid)
        details =Jobdetails.objects.get(job_id=id)
        empprofileid=details.cmp_id
        empprofile=EmployeerProfile.objects.get(user_id=empprofileid)
        jobid=details.job_id
        jobseekerprofie_id=jobseekerprofie.id
        if request.method == 'POST':
            cv=request.FILES.get('resume')
            # jobid=request.POST.get('job_id')
            jobapplicaion= JobapplicationDetails(
                applicant_resume=cv,
                jobseekerprofile_id=jobseekerprofie_id,
                job_id=jobid,
                employerprofile_id=empprofile.id
                )          
            jobapplicaion.save()
            return redirect(reverse('jobsindetail',args=[jobid]))
        else:
            
            applied = False
            if  JobapplicationDetails.objects.all() is not None:
                try:
                    applicationdetails=JobapplicationDetails.objects.get(jobseekerprofile_id=jobseekerprofie_id,job_id=jobid)
                    applied=True
                except JobapplicationDetails.DoesNotExist:
                    pass

            profiledetails=EmployeerProfile.objects.all()
            publisheddate=details.publisheddate
            formatDate = publisheddate.strftime("%d-%b-%y")
            context ={
                "job_title":details.job_title,
                "type": details.job_type,
                "description":details.job_description,
                "lastdate":details.lastdate,
                # "specialisation":details.specialisation,
                # "salary":details.expected_salary,
                # "experience":details.experience,
                "vaccancies":details.vacancies,
                # "qualification":details.qualification,
                "company_id":details.cmp_id_id,
                "profiledetails":profiledetails,
                "publisheddate":formatDate,
                "jobid":details.job_id,
                "applied":applied,
            }

            return render(request,'jobseeker/jobdetails.html',context)
            
    return redirect('loginpage')



def editprofile(request):
    if request.user.is_authenticated:
        userid = request.user.id
        jobseek = JobseekerProfile.objects.get(user_id=userid)

        jobseekprofile_id = jobseek.id
        profileidexist = None

        email = request.user.email

        if request.method == 'POST':
            profile_photo = request.FILES.get('customFile')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            phone = request.POST.get('phone')
            highestqualification = request.POST.get('highestqualification')
            experience = request.POST.get('experience')
            age = request.POST.get('age')
            cgpa = request.POST.get('cgpa')
            aboutyourself = request.POST.get('aboutyourself')
            fulladdress = request.POST.get('fulladdress')
            skills = request.POST.get('skills')

            # Update the fields and save the object
            jobseek.profile_photo = profile_photo
            jobseek.first_name = first_name
            jobseek.last_name = last_name
            jobseek.phone_number = phone
            jobseek.email = email
            jobseek.highestqualification = highestqualification
            jobseek.experience = experience
            jobseek.cgpa = cgpa
            jobseek.age = age
            jobseek.aboutyourself = aboutyourself
            jobseek.fulladdress = fulladdress
            jobseek.skills = skills
            jobseek.save()

            # Update or create the skills
            # candidateSkillsandTechnologies.objects.update_or_create(
            #     profile_id_id=jobseekprofile_id,
            #     defaults={
            #         'skill_name': skills
            #     }
            # )

            return redirect(editprofile)

        else:
            if jobseekprofile_id is not None:
                try:
                    profileidexist = candidateSkillsandTechnologies.objects.get(profile_id_id=jobseekprofile_id)
                except candidateSkillsandTechnologies.DoesNotExist:
                    pass

            context = {
                "profile_photo": jobseek.profile_photo,
                "first_name": jobseek.first_name,
                "last_name": jobseek.last_name,
                "phone": jobseek.phone_number,
                "email": jobseek.email,
                "highestqualification": jobseek.highestqualification,
                "experience": jobseek.experience,
                "cgpa": jobseek.cgpa,
                "age": jobseek.age,
                "aboutyourself": jobseek.aboutyourself,
                "fulladdress": jobseek.fulladdress,
                "skills": jobseek.skills,
                # "skills": profileidexist.skill_name if profileidexist is not None else None,
            }
            return render(request, 'jobseeker/jobseekerprofile.html', context)
    else:
        return redirect('loginpage')

def appliedjobs(request):
    userid=request.user.id
    profileid=JobseekerProfile.objects.get(user_id=userid)
    appliedjobs = JobapplicationDetails.objects.filter(jobseekerprofile_id=profileid)



    jobdetails=Jobdetails.objects.all()
    empprofiledetails = EmployeerProfile.objects.all()
    context={
        "appliedjobs":appliedjobs,
        "jobdetails":jobdetails,
        "employerprofile":empprofiledetails, 
        
    }

    return render(request,'jobseeker/appliedjobs.html',context)

def appliedjobstatus(request,id):
    user_id = request.user.id
    profile = JobseekerProfile.objects.get(user_id=user_id)
    profile_id=profile.id
    jobdetails=Jobdetails.objects.get(job_id=id)
    job_applications = JobapplicationDetails.objects.get(jobseekerprofile_id=profile_id,job_id=id)
 
    employerid=jobdetails.cmp_id_id
    employeedetails=EmployeerProfile.objects.all()
    
    context = {
        "job_details": jobdetails,
        "type":jobdetails.job_type,
        "job_title":jobdetails.job_title,
        "job_applications": job_applications,
        "employeedetails":employeedetails,
        "employerid":employerid,
       
    
    }

    return render(request, 'jobseeker/appliedjobstatus.html', context)

# def jobseekerchatbox(request,id):
#         userid=request.user.id
#         jobprofile=JobseekerProfile.objects.get(user_id=userid)
#         empprofiledetails=EmployeerProfile.objects.get(id=id)
#         context={
#             "profilelogo":jobprofile.profile_photo,
#             "profileid":id,
#             "companyname":empprofiledetails.company_name,
#             "companyphoto":empprofiledetails.company_logo,
#             "loggeduserid":userid,
#             "senttouserid":empprofiledetails.user_id,
#             "jobprofile":jobprofile,
#         }

#         return render(request,'jobseeker/jobseekerchatbox.html',context) 


def resumebuilderhomepage(request):
    return render(request,"jobseeker/resumebldrhomepage.html")




### Currently Payemnt Not Integrated


# razorpay_client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
 
# def payementpage(request):
#     userid=request.user.id
#     profiledetails=JobseekerProfile.objects.get(user_id=userid)
#     payementdetails=PayementDetails.objects.get(profile_id=userid)
#     profile_id=profiledetails.id
#     if (payementdetails.paid==1):
#         return redirect('resumebuilderhomepage')
#     else:
#         amount=30000
#         client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
#         response_payment=client.order.create(dict(amount=amount,currency='INR',payment_capture=1))
#         order_id=response_payment['id']
#         context={
#             'amount':amount,
#             'api_key':settings.RAZOR_KEY_ID,
#             'order_id':order_id,
#             'username': profiledetails.first_name,
#             'profileid':profile_id,
#             'userid':userid
#         }
#         print(response_payment)
#         return render(request,'jobseeker/payementpage.html',context)


# def verifypayment(request):
#     if request.method == 'POST':
#         razorpay_payment_id = request.POST.get('razorpay_payment_id')
#         razorpay_order_id = request.POST.get('razorpay_order_id')
#         razorpay_signature = request.POST.get('razorpay_signature')
#         amount=request.POST.get('amount')
#         amount=int(amount)/100
#         username= request.POST.get('username')
#         userid=request.POST.get('userid')
#         client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
#         try:
#             params_dict = {
#                 'razorpay_order_id': razorpay_order_id,
#                 'razorpay_payment_id': razorpay_payment_id,
#                 'razorpay_signature': razorpay_signature
#             }
#             client.utility.verify_payment_signature(params_dict)
#             PayementDetails.objects.filter(profile_id=userid).update(
#                 user_name=username,
#                 order_id=razorpay_order_id,
#                 productname="Resume Builder",
#                 amount=amount,
#                 razorpay_payment_id=razorpay_payment_id,
#                 paid=1,
#                 )
                
#             return JsonResponse({'status': 'Success'})
#         except:
#             return  JsonResponse({'status': 'Verification failed'})
#            # return HttpResponse("Payment verification failed")
#     else:
#         return HttpResponse("Invalid request method")


    

@csrf_exempt
def success(request):
    return render(request,"success.html")

def resumebldrhomepage(request):
    return render(request,"resumebldrhomepage.html")
def thankyou(request):
    return render(request,"thankyou.html")
    
def notifications(request):

     userid=request.user.id
     jobseekerprofile=JobseekerProfile.objects.get(user_id=userid)
     applicationdetails=JobapplicationDetails.objects.filter(jobseekerprofile_id=jobseekerprofile.id)

    
     application_ids = [app.application_id for app in applicationdetails]

   

     interviewscheduling = Interviewscheduling.objects.filter(application_id__in=application_ids)

     job_ids=[job.job_id for job in interviewscheduling]

     jobdetails=Jobdetails.objects.all()

     context={
         "applicationdetails":  applicationdetails,
         "interviewscheduling":interviewscheduling,
         "jobdetails":jobdetails,
         "jobids":job_ids,
   }

     return render(request,"notifications.html",context) 




########End of Payment Code


def premiumservices(request):
    return render(request,'premiumservices.html') 

def resumebuilderform(request):
    context = {'YEAR_CHOICES': [(year, year) for year in range(1900, 2100)]}
    userid=request.user.id
    profileid=JobseekerProfile.objects.get(user_id=userid)
    resumetitle=request.POST.get('resumetitle')  
    name = request.POST.get('name')    
    careerobjective = request.POST.get('careerobjective') 
    address = request.POST.get('address')    
    phonenumber = request.POST.get('phonenumber') 
    email = request.POST.get('email')    
    skills= request.POST.get('skills') 
    projecttitle=request.POST.get('projecttitle') 
    projectdescription=request.POST.get('projectdescription') 
    profilepic = request.FILES.get('profilepic')
    collegename=request.POST.get('collegename') 
    coursename=request.POST.get('coursename') 
    passingyear = request.POST.get('collegepassingyear')

    twelthschoolname=request.POST.get('schoolname') 
    twelthmarks=request.POST.get('hssmarks') 
    twelthpassingyear = request.POST.get('hsspassingyear')
    tenthschoolname=request.POST.get('hsschoolname') 
    tenthmarks=request.POST.get('tenthmarks') 
    tenthpassingyear = request.POST.get('tenthpassingyear')
    if request.method == 'POST':
        resumedetails=ResumeSchema(
            resumetitle=resumetitle,
            seekername=name,
            careerobjective=careerobjective,    
            address=address,
            phonenumber=phonenumber,
            email=email,
            skills=skills,
            projecttitle=projecttitle,
            projectdescription=projectdescription,
            profilepicture=profilepic,
            collegename=collegename,
            coursename=coursename,
            passingyear=passingyear,
            hssname=twelthschoolname,
            hssyear=twelthpassingyear,
            hssmarks=twelthmarks,
            tenthschoolname=tenthschoolname,
            tenthpassyear=tenthpassingyear,
            tenthmarks=tenthmarks,
            jprofile_id=profileid.id
        )
        resumedetails.save()
        value=ResumeSchema.objects.get(resume_id=resumedetails.pk)
        messages.success(request,"Resume Created")
        return redirect(reverse('resumepreview',args=[value.resume_id]))
   

        # return render(request, 'jobseeker/resumebuilderform.html',context)
    # else:
       
    return render (request, 'resumebuilderform.html',context)



def resumepreview(request, id): #show resume of requested id
    userid=request.user.id
    profileid=JobseekerProfile.objects.get(user_id=userid)
    allresumes = ResumeSchema.objects.get(jprofile_id=profileid.id,resume_id=id)
    context={
        "allresumes":allresumes
    }
    return render(request, 'resumepreview.html',context)

def deleteresume(request,id):
    userid=request.user.id
    profileid=JobseekerProfile.objects.get(user_id=userid)
    allresumes = ResumeSchema.objects.get(jprofile_id=profileid.id,resume_id=id)
    allresumes.delete()
    return redirect(request.META.get('HTTP_REFERER'))
    

def resumelist(request): #show resume of requested id
    userid=request.user.id
    profileid=JobseekerProfile.objects.get(user_id=userid)
    allresumes = ResumeSchema.objects.filter(jprofile_id=profileid.id)
    context={
        "allresumes":allresumes
    }
    return render(request,'resumelist.html',context)

def userpaymentdetails(request):

    userid=request.user.id
    # userpayementdetails=PayementDetails.objects.filter(profile_id=userid)
    query = Q(razorpay_payment_id__isnull=False) & Q(order_id__isnull=False) & Q(profile_id=userid)
    userpayementdetails = PayementDetails.objects.filter(query)
    context={
        "userpayementdetails":userpayementdetails
    }
    
    return render(request,'userpaymentdetails.html',context)


# def coverletterhomepage(request):
#     return render(request,"jobseeker/coverletterhomepage.html")



# def coverletterform(request):
#     userid=request.user.id
#     profileid=JobseekerProfile.objects.get(user_id=userid)
#     coverlettertitle=request.POST.get('covertitle')  
#     candidatename = request.POST.get('name')    
#     role_you_apply = request.POST.get('designation') 
#     company_apply = request.POST.get('companyname')    
#     skills= request.POST.get('skills') 


#     prompt = f"Generate cover letter for applicant name {candidatename} and I am applying for the position of {role_you_apply} at {company_apply}. I have experience in {skills}."
#     response = openai.Completion.create(
#         model="text-davinci-003", 
#         prompt=prompt,
#         temperature=0.5,
#         max_tokens=1024
#         )
#     completion_text = response.choices[0].text
#     print(completion_text)
#     if request.method == 'POST':
#             letterdetails=CoverLetterDetails(
#             coverlettertitle=coverlettertitle,
#             profile_id=  profileid.id,
#             coverletter=completion_text,
#             )
#             letterdetails.save()
#             # value=CoverLetterDetails.objects.get(coverletter_id=letterdetails.pk)
#             # return redirect(reverse('resumepreview',args=[value.coverletter_id]))
           
#     return render(request,"jobseeker/coverletterform.html")


# def allcoverletter(request):
#     userid=request.user.id
#     profileid=JobseekerProfile.objects.get(user_id=userid)
#     coverletters=CoverLetterDetails.objects.filter(profile_id=profileid.id)
#     context={
#         "coverletters":coverletters
#     }
#     return render(request,"jobseeker/allcoverletters.html",context)


# def coverletterpreview(request,id):
#     userid=request.user.id
#     profileid=JobseekerProfile.objects.get(user_id=userid)
#     coverletters=CoverLetterDetails.objects.get(coverletter_id=id)
#     context={
#         "coverletters":coverletters
#     }

#     return render(request,"jobseeker/coverletterpreview.html",context)



#To render different User Home pages

def adminpage(request):
    if request.user.is_authenticated:
        jobseekercount = JobseekerProfile.objects.all().count()
        actualcount=jobseekercount-1
        employeercount = EmployeerProfile.objects.all().count()
        context={
        'employeercount':employeercount,
        'jobseekercount':actualcount,
        }

        return render(request,'moderator/admin.html',context)
    else:
        return redirect('loginpage')



@login_required(login_url='/login')
def employeerpage(request):

    id = request.user
    postedjobcount = Jobdetails.objects.filter(cmp_id_id=id).count()
    context={
    'postedjobcount':postedjobcount
    }

    return render(request,'employeer/home.html',context)





# Admin Pages


def employerslist(request):
    employees = User.objects.filter(role="EMPLOYEER").select_related('employeerprofile','verificationdetails')
    context={
        "employees":employees,
    }
    return render(request,'moderator/employerslist.html',context) 

def jobseekerslist(request):
    seekers = User.objects.filter(role="JOBSEEKER")
    context={
        "seekers":seekers
    }
    return render(request,'moderator/jobseekerslist.html',context) 


def employerdetails(request,id):
    if request.user.is_authenticated:

        profiledetails = EmployeerProfile.objects.get(user_id=id)
        verificationdetails = Verificationdetails.objects.get(user_id=id)
        userdetails = User.objects.get(id=id)
        context = {
           
            'company_name':profiledetails.company_name,
            'officelocation':profiledetails.office_location,
            'phonenumber':profiledetails.phone_number,
            'address':profiledetails.address,
            'buisnesslicense':verificationdetails.buisnesslicence,
            'email':userdetails.email,
            'username':userdetails.username,
            'companylogo':profiledetails.company_logo,
            'status':verificationdetails.isverified,
            'id':userdetails.id
        }


        return render(request,'moderator/employeerdetails.html',context)
    return redirect('loginpage')


def accept(request,id):
    xy = Verificationdetails.objects.get(user_id=id)
    status_value = xy.isverified
    if status_value == 0:
        xy.isverified=1
        xy.save()
    
    return redirect(request.META.get('HTTP_REFERER'))

def reject(request,id):
    xy = Verificationdetails.objects.get(user_id=id)
    status_value = xy.isverified
    if status_value == 1:
        xy.isverified=0
        xy.save()

    return redirect(request.META.get('HTTP_REFERER'))



# def allpayements(request):

#     query = Q(razorpay_payment_id__isnull=False) & Q(order_id__isnull=False)
#     results = PayementDetails.objects.filter(query)
#     context={
#         "results":results
#     }
#     return render(request,'moderator/allpayements.html',context)

# def statistics(request):
#     return render(request,'moderator/statisticshome.html')


# def reports(request):
#     return render(request,'moderator/reportshome.html')

from django.shortcuts import render
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest


# authorize razorpay client with API Keys.
razorpay_client = razorpay.Client(
	auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))


from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest
from django.conf import settings

# Assuming razorpay_client is properly configured
# and imported

def payment(request):
    currency = 'INR'
    amount = 20000  # Rs. 200

    # Create a Razorpay Order
    razorpay_order = razorpay_client.order.create(dict(amount=amount,
                                                       currency=currency,
                                                       payment_capture='0'))

    # order id of newly created order.
    razorpay_order_id = razorpay_order['id']
    callback_url = '/paymenthandler/'

    # we need to pass these details to frontend.
    context = {}
    context['razorpay_order_id'] = razorpay_order_id
    context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
    context['razorpay_amount'] = amount
    context['currency'] = currency
    context['callback_url'] = callback_url

    return render(request, 'payment.html', context=context)

def paymentintern(request):
    currency = 'INR'
    amount = 20000  # Rs. 200

    # Create a Razorpay Order
    razorpay_order = razorpay_client.order.create(dict(amount=amount,
                                                       currency=currency,
                                                       payment_capture='0'))

    # order id of newly created order.
    razorpay_order_id = razorpay_order['id']
    callback_url = '/internhandler/'

    # we need to pass these details to frontend.
    context = {}
    context['razorpay_order_id'] = razorpay_order_id
    context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
    context['razorpay_amount'] = amount
    context['currency'] = currency
    context['callback_url'] = callback_url

    return render(request, 'payment.html', context=context)

# csrf_exempt decorator to disable CSRF protection
@csrf_exempt
def paymenthandler(request):
    # only accept POST request.
    if request.method == "POST":
        # get the required parameters from post request.
        payment_id = request.POST.get('razorpay_payment_id', '')
        razorpay_order_id = request.POST.get('razorpay_order_id', '')
        signature = request.POST.get('razorpay_signature', '')
        params_dict = {
            'razorpay_order_id': razorpay_order_id,
            'razorpay_payment_id': payment_id,
            'razorpay_signature': signature
        }
        # verify the payment signature.
        result = razorpay_client.utility.verify_payment_signature(
            params_dict)
        if result is not None:
            amount = 20000  # Rs. 200
            # capture the payment
            razorpay_client.payment.capture(payment_id, amount)
            # render success page on successful capture of payment
            return render(request, 'resumebuilderform.html')
        else:
            # if signature verification fails.
            return render(request, 'paymentfail.html')
    else:
        print(5)
        # if other than POST request is made.
        return HttpResponseBadRequest()

# csrf_exempt decorator to disable CSRF protection
@csrf_exempt
def internhandler(request):
    # only accept POST request.
    if request.method == "POST":
        # get the required parameters from post request.
        payment_id = request.POST.get('razorpay_payment_id', '')
        razorpay_order_id = request.POST.get('razorpay_order_id', '')
        signature = request.POST.get('razorpay_signature', '')
        params_dict = {
            'razorpay_order_id': razorpay_order_id,
            'razorpay_payment_id': payment_id,
            'razorpay_signature': signature
        }
        # verify the payment signature.
        result = razorpay_client.utility.verify_payment_signature(
            params_dict)
        if result is not None:
            amount = 20000  # Rs. 200
            # capture the payment
            razorpay_client.payment.capture(payment_id, amount)
            # render success page on successful capture of payment
            return render(request, 'thankyou.html')
        else:
            # if signature verification fails.
            return render(request, 'paymentfail.html')
    else:
        print(5)
        # if other than POST request is made.
        return HttpResponseBadRequest()


from django.shortcuts import render

def resume(request):
    return render(request, 'resume.html')

import pyttsx3
import re
from nltk.corpus import stopwords
from nltk.sentiment import SentimentIntensityAnalyzer

# views.py
def my_form(request):
    engine = pyttsx3.init()
    engine.say('Hello, Welcome to the feedback section.')
    engine.runAndWait()
    return render(request,'form.html')
 

def my_post(request):
        if request.method == 'POST':
                stop_words = stopwords.words('english')
                # my contribution
                stop_words.remove('very')
                stop_words.remove('not')
                
                #convert to lowercase
                text1 = request.POST['text1'].lower()
                
                # my contribution
                text_final = ''.join(i for i in text1 if not i.isdigit())
                net_txt=re.sub('[^a-zA-Z0-9\n]', ' ',text_final)
                
                #remove stopwords    
                processed_doc1 = ' '.join([i for i in net_txt.split() if i not in stop_words])

                sa = SentimentIntensityAnalyzer()
                dd = sa.polarity_scores(text=processed_doc1)
                compound = round((1 + dd['compound'])/2, 2)
                final=compound*100
                
                if "enough" in text1 or "sufficient" in text1 or "ample" in text1 or "abudant" in text1:
                   engine = pyttsx3.init()
                   engine.say('You liked us by'+str(final)+'% Thank you for your valuable response')
                   engine.runAndWait()
                   feeds = feedback(feedback=text1,percentage=final,good=True,bad=True,neutral=False)
                   feeds.can_id =request.user
                   feeds.save()
                   return render(request,'form.html',{'final': final,'text1':net_txt})
                   
                elif final == 50:
                   engine = pyttsx3.init()
                   engine.say('Please enter an adequate resposnse, Thank You')
                   engine.runAndWait()
                   return render(request,'form.html',{'final': final,'text1':net_txt})
                else:
                   engine = pyttsx3.init()
                   engine.say('You liked us by'+str(final)+'% Thank you for your valuable response')
                   engine.runAndWait()
                   if final > 50:
                      feeds = feedback(feedback=text1,percentage=final,good=False,bad=True,neutral=True)
                      feeds.can_id =request.user
                      feeds.save()
                      return render(request,'form.html',{'final': final,'text1':net_txt})
                   elif final < 50:
                      feeds = feedback(feedback=text1,percentage=final,bad=False,good=True,neutral=True)
                      feeds.can_id =request.user
                      feeds.save()
                      return render(request,'form.html',{'final': final,'text1':net_txt})
                   else:
                       feeds = feedback(feedback=text1,percentage=final)
                       feeds.can_id =request.user
                       feeds.save()
                       return render(request,'form.html',{'final': final,'text1':net_txt})
        else:
           return redirect('my_form')

def feedbacks(request):
    feed=feedback.objects.all()
    context = {'feed': feed}
    return render(request,"feedbackview.html", context)

# def inadd(request):
#     if 'emp' in request.session:
#        return render(request,"inadd.html")
#     return render(request,'inadd.html')

# # def moreinterns(request,id):
# #     feed=internship.objects.all()
# #     print(feed)
# #     for i in feed:
# #         print(i)
# #     more=classdetails.objects.filter(candi_id=id)
# #     context = {'feed': feed,'more':more}
# #     return render(request,"moreinterns.html", context)

# def interinfo(request):
#     if 'can' in request.session:
#        inid=request.POST.get('inid')
#        data=internship.objects.filter(intern_id=inid)
#        return render(request,"interinfo.html",{'data':data})
#     return render(request,'interinfo.html')


# def classdetail(request):
#     inid= request.POST['inid']
#     caid= request.POST['caid']
#     more=classdetails.objects.filter(candi_id=caid,inter_id=inid)
#     feed=internship.objects.filter(intern_id=inid)
#     can=User.objects.get(id=caid)
#     inter=internship.objects.get(intern_id=inid)
#     # user = classdetails(candi_id=caid,inter_id=inid,interndate,interntimes)
#     # user.save()
#     return render(request,'classdetails.html',{'can':can.username,'inter':inter.title,'interid':inter.intern_id,'more':more,'feed':feed,'mo':inid,'mor':caid})

# def intern1(request):
#       if request.method == 'POST':
#         tit = request.POST['tit']
#         cap = request.POST['cap']
#         durno = request.POST['durno']
#         durex = request.POST['durex']
#         sdate = request.POST['sdate']
#         edate = request.POST['edate']
#         caty = request.POST['caty']
#         loc = request.POST['loc']
#         ofon = request.POST['ofon']
#         about = request.POST['about']
#         stip = request.POST['stip']
#         wca = request.POST['wca']
#         image = request.FILES.get('p')
#         member = internship(title=tit,caption=cap,durno=durno,durex=durex,stdate=sdate,enddate=edate,img=image,category=caty,location=loc,onoff=ofon,stipend=stip,whoapply=wca,moreinfo=about)
#         member.save()
#         return redirect('inadd')
# def contentlist(request):
#     adconts=internship.objects.all()
#     return render(request,'moreinterns.html',{'adconts': adconts})
# def candidateintern(request):
#     adconts=internship.objects.all()
#     return render(request,'candiateintern.html',{'adconts': adconts})

# def moreinterns(request):
#     internship_obj = internship.objects.all()
#     return render(request, 'moreinterns.html', {'internship': internship_obj})
from .models import Interndetails
from django.shortcuts import render, redirect
from django.contrib import messages

from django.urls import reverse
def postintern(request):
    userid = request.user.id
    vdetails = Verificationdetails.objects.get(user_id=userid)
    value = vdetails.isverified
    if request.method == 'POST':
        jobtitle = request.POST.get('job_title')
        jobdescription = request.POST.get('job_description')
        duration = request.POST.get('duration')
        location = request.POST.get('location')
        mode = request.POST.get('mode')
        stipend = request.POST.get('stipend')
        whocanapply = request.POST.get('whocanapply')
        startdate = request.POST.get('start_date')
        lastdate = request.POST.get('end_date')

        # Create an instance of Interndetails and save it to the database
        posted_job = Interndetails.objects.create(
            title=jobtitle,
            description=jobdescription,
            duration=duration,
            location=location,
            mode=mode,
            stipend=stipend,
            whocanapply=whocanapply,
            startdate=startdate,
            lastdate=lastdate
        )

        # Set the cmp_id field to the current user's ID
        posted_job.cmp_id = request.user

        # Save the changes
        posted_job.save()

        messages.success(request, "Posted Successfully")
        return redirect(reverse('manageintern', args=[userid]))
    else:
        current_value = request.user
        user_id = current_value.id
        context = {
            'user_id': user_id,
            'verified': value,
        }
        return render(request, 'postintern.html', context)

def editintern(request, id):
        jb = Interndetails.objects.get(pk=id)
        idvalue = request.user
        # allqualifications = Qualifications.objects.filter(cmp_id_id=idvalue)
        if request.method == 'POST':
            jobtitle = request.POST.get('job_title')
            jobdescription = request.POST.get('job_description')
            duration = request.POST.get('duration')
            location = request.POST.get('location')
            mode = request.POST.get('mode')
            stipend = request.POST.get('stipend')
            whocanapply = request.POST.get('whocanapply')
            startdate = request.POST.get('start_date')
            lastdate = request.POST.get('end_date')
            
            Jobdetails.objects.filter(job_id=id).update(
                title=jobtitle,
                description=jobdescription,
                duration=duration,
                location=location,
                mode=mode,
                stipend=stipend,
                whocanapply=whocanapply,
                startdate=startdate,
                lastdate=lastdate
            )
            value = jb.cmp_id_id
            return redirect(reverse('manageintern', args=[value]))
        else:
            jobtitle = jb.title
            jobdescription = jb.description
            duration = jb.duration
            location = jb.location
            mode = jb.mode
            stipend = jb.stipend
            whocanapply = jb.whocanapply
            startdate = jb.startdate
            lastdate = jb.lastdate

            context = {
                'detail': jb,
                'jobtitle': jobtitle,
                'jobdescription': jobdescription,
                'duration': duration,
                'mode': mode,
                'stipend': stipend,
                'whocanapply': whocanapply,
                'startdate': startdate,
                'lastdate': lastdate,
            }
            return render(request, 'editintern.html', context)



from .models import Interndetails  # Import the Interndetails model

from .models import Interndetails

def manageintern(request, id):
    if request.user.is_authenticated:
        # Filter Interndetails based on the company field
        pos = Interndetails.objects.filter(company=id)  
        if request.method == 'POST':
            searched = request.POST.get('searched')
            # Filter Interndetails by job_title containing the searched keyword
            jobs = Interndetails.objects.filter(title__contains=searched)
            for i in jobs:
                print(i.title)
            context = {
                'searched': searched,
                'jobs': jobs,
            }
            return render(request, 'manageintern.html', context)
        else:
            context = {
                'pos': pos,
                'id': id
            }
            return render(request, 'manageintern.html', context)
    return redirect('loginpage')


from django.shortcuts import render, redirect
from django.utils import timezone
from .models import Interndetails
from app1.models import EmployeerProfile, JobseekerProfile, candidateSkillsandTechnologies, JobapplicationDetails

def intern(request):
    if request.user.is_authenticated:
        userid = request.user.id
        jobseekerprofile = JobseekerProfile.objects.get(user_id=userid)
        profile_id = jobseekerprofile.id  

        try:
            jobseekerskills = candidateSkillsandTechnologies.objects.get(id=profile_id)
            jobseeker_skills = jobseekerskills.skill_name
            jobseeker_skill_list = [s.strip() for s in jobseeker_skills.split(',')]
        except candidateSkillsandTechnologies.DoesNotExist:
            jobseeker_skill_list = []

        current_date = timezone.now().date()
        applied_jobs = JobapplicationDetails.objects.filter(jobseekerprofile=jobseekerprofile).values_list('job_id', flat=True)
        internship_details = Interndetails.objects.exclude(id__in=applied_jobs)

        profiledetails = EmployeerProfile.objects.all()

        if request.method == 'POST':
            searched = request.POST.get('searched')
            jobs = internship_details.filter(title__contains=searched)
            context = {
                'searched': searched,
                'jobs': jobs,
                'profiledetails': profiledetails,
            }
            return render(request, 'intern.html', context) 
        else:
            context = {
                'interndetails': internship_details,
                'profiledetails': profiledetails,
                'jobseeker_skill_list': jobseeker_skill_list,
            }
            return render(request, 'intern.html', context)
    else:
        return redirect('loginpage')



    
from .models import Interndetails  # Correct import statement

def interndetails(request, id):
    if request.user.is_authenticated:
        try:
            internship = Interndetails.objects.get(id=id)  # Correct model name
            intern_title = internship.title
            mode = internship.mode
            description = internship.description
            duration = internship.duration
            startdate = internship.startdate
            lastdate = internship.lastdate
            stipend = internship.stipend
            whocanapply = internship.whocanapply

            context = {
                "intern_title": intern_title,
                "mode": mode,
                "description": description,
                "startdate": startdate,
                "lastdate": lastdate,
                "duration": duration,
                "stipend": stipend,
                "whocanapply": whocanapply,
            }

            return render(request, 'employeer/jobpreviewdetail.html', context)
        except Interndetails.DoesNotExist:
            return HttpResponse("Internship details not found")
    return redirect('loginpage')


from django.http import HttpResponse
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from .models import Jobdetails, EmployeerProfile

def generate_pdf_report(request):
    # Fetch job details and employer profiles
    jobdetails = Jobdetails.objects.all()
    profiledetails = EmployeerProfile.objects.all()

    # Define data for the PDF report table
    data = [['Job Title', 'Company', 'Location', 'Job Type', 'Last Date']]

    for job in jobdetails:
        company_name = None
        for profile in profiledetails:
            if job.cmp_id_id == profile.user_id:
                company_name = profile.company_name
                break

        data.append([
            job.job_title,
            company_name,
            job.office_location,
            job.job_type,
            str(job.lastdate),
        ])

    # Create PDF document
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="job_report.pdf"'

    doc = SimpleDocTemplate(response, pagesize=letter)
    table = Table(data)

    # Add style to the table
    style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                        ('GRID', (0, 0), (-1, -1), 1, colors.black)])

    table.setStyle(style)

    # Add table to the PDF document
    doc.build([table])

    return response
