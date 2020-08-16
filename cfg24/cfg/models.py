from django.db import models
from jsonfield import JSONField


# Create your models here.
class Student(models.Model):
    email = models.EmailField(max_length=254)
    objective = models.TextField()
    education = models.TextField()
    miscellaneous = models.TextField()
    password=models.CharField(max_length=20)
    name=models.CharField(max_length=100)
    student_id=models.IntegerField()
    courses=JSONField()
    test_names=JSONField()
    courses=JSONField()
    skill_set=JSONField()
    coursesnum=models.IntegerField()
class Teacher(models.Model):
    password=models.CharField(max_length=50)
    name=models.CharField(max_length=100)
    teacher_id=models.IntegerField()
class Course(models.Model):
    name=models.CharField(max_length=100)
    links=JSONField()
    modules=JSONField()
class Quiz(models.Model):
    title=models.CharField(max_length=100)
    max_marks=models.IntegerField()
    links=JSONField()

    
    