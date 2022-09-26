from email import feedparser
from django.db import models
from django.contrib.auth.models import AbstractUser



class Classroom(models.Model):
    roomID = models.AutoField(primary_key=True)
    code = models.CharField(max_length= 100)
    status = models.CharField(max_length= 100)
    teacher = models.CharField(max_length= 100)
    student = models.CharField(max_length= 100)

class Quiz(models.Model):
    quiID = models.AutoField(primary_key=True)
    question = models.CharField(max_length= 2000)
    subject = models.CharField(max_length= 2000)
    teacherID = models.CharField(max_length= 100)
    answerOne = models.CharField(max_length= 100)
    answerTwo = models.CharField(max_length= 100)
    answerThree = models.CharField(max_length= 100)
    answerFour = models.CharField(max_length= 100)

class User(AbstractUser):
    userID = models.AutoField(primary_key=True)
    firstname = models.CharField(max_length= 100)
    lastname = models.CharField(max_length= 100)
    phone_number = models.CharField(max_length=11)
    email = models.CharField(max_length=100)

    class meta:
        db_table = 'tbluser'