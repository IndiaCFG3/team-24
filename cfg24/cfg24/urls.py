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
from . import views
urlpatterns = [
    path('admin/', admin.site.urls),
    #path('teacherlanding/',views.,name="teacherlanding"), # intial page for teacher 
    # path('courses/',views.,name="courses"),
    #path('addcourse/',views.,namae="addcourse"),
    #path('updatecourse/',views.,name="updatecourse"),
    #path('tests/',views., name ="tests"),
    #path('generatedresume',views.,name="resume"),
    #path('certificate',views.,namme="certificate"),
    #path('quiz',views.,name="quiz"),
    #path('addquiz',views.,name="quiz"),



    path('logout',views.logout_view, name = "logout"),

]
