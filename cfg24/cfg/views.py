from django.shortcuts import render, redirect,get_object_or_404
from .models import *
from django.http import HttpResponse, JsonResponse,Http404
from rest_framework.decorators import api_view
from django.views.decorators.http import require_POST
import json
from django.views.decorators.csrf import csrf_exempt
# from .forms import *
from django.contrib.auth import login, authenticate, logout
import re
from .decorators import *
# from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

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


def login_student(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user:
        login(request, user)
        student = Student.objects.get(name = username)
        return render(request,'StudentDashboard.html',{'student':student})

def logout_view(request):
	logout(request)
	return redirect('signup')

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
    courses = Courses.objects.all()
    return render(request,'Courses.html',{'courses':courses})

def register_course(request):
    new_course = Courses()
    new_course.name = request.POST['coursename']
    #request.

#def resume_to_pdf(request):