from django.db import models 
from django.contrib.auth.models import User
from django.forms import ModelForm
   
class Student(models.Model):
    usn=models.CharField(max_length=10) 
    name=models.CharField(max_length=20) 
    sem=models.IntegerField() 
    sec=models.CharField(max_length=1)
    gender=models.CharField(max_length=1)
    phone=models.CharField(max_length=10)
    email=models.CharField(max_length=30)
    password=models.CharField(max_length=30)

class Team(models.Model):
    t_id=models.AutoField(primary_key=True)
    title=models.CharField(max_length=50)
    member1=models.CharField(max_length=10)
    member2=models.CharField(max_length=10)
    member3=models.CharField(max_length=10)
    member4=models.CharField(max_length=10)
    def __str__(self): 
        return self.title 
    class Meta:
        verbose_name = 'Team'
        verbose_name_plural = 'Teams'

class Project(models.Model):
    p_id=models.AutoField(primary_key=True)
    t_id=models.ForeignKey(Team,on_delete=models.CASCADE) 
    domain=models.CharField(max_length=50)
    title=models.CharField(max_length=50,default="")
    abstract=models.CharField(max_length=50,default="")
    synopsis=models.FileField()
    report=models.FileField()

class Weeklyreport(models.Model):
    p_id=models.ForeignKey(Project,on_delete=models.CASCADE)
    week_no=models.IntegerField()
    date=models.DateField()
    summary=models.CharField(max_length=200)

class Schedule(models.Model):
    s_id=models.AutoField(primary_key=True)
    event=models.CharField(max_length=20)
    date=models.DateField()
    instrution=models.CharField(max_length=200)
    deadline=models.DateField()

class Synopsis(ModelForm): 
    required_css_class="required" 
    class Meta: 
        model=Project 
        fields=['t_id'] 
