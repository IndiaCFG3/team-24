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
