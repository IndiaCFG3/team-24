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
        if Student.objects.filter(email=email).exists():
            student=Student.objects.filter(email=email)
            if student.password==password1:
                redirect('')
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
    student = request.user

    return render(request, 'StudentDashboard.html',{'student':student})

def teacher_home(request):
    teacher = request.user
    return render(request, 'StudentDashboard.html',{'teacher':teacher})

def add_course(request,course_id):
    course=get_object_or_404(Course,pk=course_id)
    student = Student.objects.get(name=request.user.username)#TBC
    student_courses = json.loads(student.courses)
    student_courses[len(student_courses)+1] = {'course':course,'complete':False}
    student_courses = json.dump(student_courses)
    student.courses = student_courses
    student.save()
    return render(request,'StudentDashboard.html') #message to be added later

def view_courses(request):
    courses = CourseVideos.objects.all()
    return render(request,'Courses.html',{'courses':courses})

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