from django.db import models

# Create your models here.
class Student(models.Model):
    email = models.EmailField(max_length=254)
    password=models.CharField(max_length=20)
    name=models.CharField(max_length=100)
    student_id=models.IntegerField()
    courses=models.JSONField()
    test_names=models.JSONField()
    courses=models.JSONField()
    skill_set=models.JSONField()
    coursesnum=models.IntegerField()
class Teacher(models.Model):
    password=models.CharField(max_length=50)
    name=models.CharField(max_length=100)
    teacher_id=models.IntegerField()
class Course(models.Model):
    name=models.CharField(max_length=100)
    links=models.JSONField()
    modules=models.JSONField()
class Quiz(models.Model):
    title=models.CharField(max_length=100)
    max_marks=models.IntegerField()
    links=models.JSONField()

    
    