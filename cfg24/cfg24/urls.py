"""cfg24 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from cfg import views
urlpatterns = [
    path('admin/', admin.site.urls),
    #path('teacherlanding/',views.,name="teacherlanding"), # intial page for teacher 
    path('courses/',views.view_courses,name="courses"),
    path('updatecourse/<str:name>',views.add_course,name="addcourse"),
    #path('tests/',views., name ="tests"),
    path('generatedresume/',views.unauth_pdf,name="resume"),
    #path('certificate',views.,namme="certificate"),
    #path('quiz',views.,name="quiz"),
    #path('addquiz',views.,name="quiz"),
    path('login-student/',views.studentlogin,name = 'student_login'),
    path('login-teacher/',views.teacherlogin,name = 'teacher_login'),
    path('register-student',views.studentregister, name = 'student-register'),
    path('register-teacher',views.teacherregister,name = 'teacher-register'),
    path('',views.home,name = 'home'),
    path('upload-videos/',views.post_courses,name = 'upload_videos'),
    path('upload/',views.upload_video,name = 'upload'),
    path('student-home/',views.student_home,name= "student_home"),
    path('teacher-home/',views.teacher_home,name= "teacher_home"),
    path('update-progress/<str:name>/',views.add_progress,name= "progress"),

    path('logout',views.logout_view, name = "logout"),

]
