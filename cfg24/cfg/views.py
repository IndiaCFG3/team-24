from django.shortcuts import render, redirect,get_object_or_404
from .models import *
from django.http import HttpResponse, JsonResponse,Http404
from rest_framework.decorators import api_view
from django.views.decorators.http import require_POST
import json
from rest_framework.decorators import api_view
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import IsAuthenticated
from rest_framework import filters
# from .forms import *
from django.contrib.auth import login, authenticate, logout
import re
#from .serializers import *
#from .decorators import *
# from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .pdf import render_to_pdf
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import smtplib
from email.mime.base import MIMEBase 
from email import encoders 
'''Registration,login,logout start'''


def teacherregister(request):
    if request.method == 'POST':
        name=request.POST['name']
        email=request.POST['email']
        username=request.POST['username']
        password1=request.POST['psw']
        password2=request.POST['psw-repeat']
        course_name=request.POST['courses']
        course={"0":course_name}
        if password1==password2:  
            if Teacher.objects.filter(email=email).exists():
                return redirect('teacherregister')
            else:
                user=Teacher.objects.create_user(name=name,username=username,password=password1,email=email,courses=course)
                user.save()
                print('user created')
                return redirect('/')
        else:
            return redirect('teacherregister')
    else:
        return render(request,'TeacherRegistration.html')

# def marksstat (request):
#     if request.method == 'GET':
#         course1=request.POST['ques1']
#         course2=request.POST['quest2']
        
        

def studentregister(request):
    if request.method == 'POST':
        name=request.POST['name']
        email=request.POST['email']
        username=request.POST['username']
        password1=request.POST['psw']
        password2=request.POST['psw-repeat']
        if password1==password2:  
            if Student.objects.filter(email=email).exists():
                return redirect('studentregister')
            else:
                user=Student.objects.create_user(name=name,username=username,password=password1,email=email,courses={})
                user.save()
                print('user created')
                return redirect('/')
        else:
            return redirect('studentregister')
    else:
        return render(request,'student_login.html')




def teacherlogin(request):
    if request.method == 'POST':
        email=request.POST['uname']
        password1=request.POST['psw']
        if Teacher.objects.filter(email=email).exists():
            teacher=Teacher.objects.filter(email=email)
            if teacher.password==password1:
                redirect('')
        else:
            return redirect('teacherregister')
    else:
        return render(request,'teacher_login.html')


def studentlogin(request):
    if request.method == 'POST':
        email=request.POST['uname']
        password1=request.POST['psw']
        student = get_object_or_404(Student, pk=1)
        if student.password == password1:
            return redirect('student_home')
        else:
            return redirect('studentregister')

    else:
        return render(request,'student_login.html')

def logout_view(request):
	logout(request)
	return redirect('signup')


def home(request):
    return render(request,'index.html')


def student_home(request):
    student = get_object_or_404(Student,pk=1)
    chapters = []
    progress = []
    courses = json.loads(student.courses)
    for i in courses:
        if i != "none":
            if i not in chapters:
                chapters.append(i)
    

    return render(request, 'StudentDashboard.html',{'student':student,'courses':chapters,})

def teacher_home(request):
    teacher = request.user
    return render(request, 'StudentDashboard.html',{'teacher':teacher})

def add_course(request,name):
    #course=CourseVideos.objects.get(chap_name = name)
    student = get_object_or_404(Student,pk=1) #TBC
    #print(student.courses)
    student_courses =json.loads(student.courses)
    if name not in student_courses:
        student_courses[len(student_courses)+1] = {'course':name,'complete':False,'progress':0.0}
        student_courses = json.dumps(student_courses)
        student.courses = student_courses
        student.save()
    return render(request,'StudentDashboard.html') #message to be added later
def add_progress(request,name):
    student = get_object_or_404(Student,pk=1)
    progress = 0.0;
    courses = json.loads(student.courses)
    for i in range(len(courses)):
        if courses[i]['course'] == name:
            courses[i]['progress'] += 1/len(courses)
            sendmailprogress(student.name, student.email, courses[i]['progress']*100)
    return redirect('student_home')
        

def view_courses(request):
    videos = CourseVideos.objects.all()
    return render(request,'course_list.html',{'courses':videos})

# def add_video(request):
#     chapter_name = request.POST[]

#def resume_to_pdf(request):
def post_courses(request):
    chapter_name  = request.POST['course']
    video = CourseVideos()
    video.chapter_name = chapter_name
    video.faculty = request.POST['faculty']
    video.link = request.POST['link']
    video.link_description = request.POST['description']
    video.save()
    return redirect('upload')

def upload_video(request):
    return render(request,"postlink.html")


    

def unauth_pdf(request, stud_id):
    print("got here", type(bill_id))
    try:
        bill = get_object_or_404(Bill, pk=bill_id)
        print(bill.id)
        order = json.loads(bill.billdetails)
        order["id"] = bill.id
        order["datetime"] = bill.date_time
        print(order)
        template = get_template("app1/pdf.html")
        html = template.render({"order": order})
        pdf = render_to_pdf("app1/pdf.html", {"order": order})  # pdf

        if pdf:
            response = HttpResponse(pdf, content_type="application/pdf")
            filename = "Invoice_{}.pdf".format(order["id"])
            content = "inline; filename = %s" % (filename)
            response["Content-Disposition"] = content
            return response
        else:
            return HttpResponse("Not Found/Error. Please try again")
    except Bill.DoesNotExist:
        return HttpResponse(
            "Sorry, that bill doesnt exist. Please check your invoice number"
        )

def sendmailprogress(name, email, progress):
    msg = MIMEMultipart()
    msg['From'] = ""
    password=''
    msg['To']= email #"info@trudawnsolutions.com" to be put once approved
    msg['Subject'] = "Progress updated!"
    msg.attach(MIMEText('<p align = "center"> {}, youre making progress!</p><p> your current progress is: {}<br>Keep Learning!</p>'.format(name,progress), 'html'))
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(msg['From'],password)
    s.sendmail(msg['From'],msg['To'],msg.as_string())
    s.quit()
