from django.shortcuts import render
from collections import namedtuple
from django.db.models.fields import EmailField
from django.http import Http404
from django.shortcuts import render, redirect
from django.views.generic import View
from django.http import HttpResponse
from .models import *
from .forms import *

# Create your views here. 
class homeView(View):
    def get(self, request):
        return render(request, 'home.html',{})

class teacherdashboardView(View):
    def get(self, request):
        return render(request, 'teacherdashboard.html',{})

class studentdashboardView(View):
    def get(self, request):
        return render(request, 'studentdashboard.html',{})
                

class aboutView(View):
    def get(self, request):
        return render(request, 'about.html',{})

class contactView(View):
    def get(self, request):
        return render(request, 'contact.html',{})

class loginView(View):
    def get(self, request):
        return render(request, 'login.html',{})

class createquizView(View):
    def get(self, request):
        return render(request, 'createquiz.html',{})

class createClassAdminView(View):
    def get(self, request):
        return render(request, 'createclassadmin.html',{})      
class createClassTeacherView(View):
    def get(self, request):
        return render(request, 'createclassteacher.html',{})    

class autoGenerateView(View):
    def get(self, request):
        return render(request, 'autogenerate.html',{})

class reviewPageView(View):
    def get(self, request):
        return render(request, 'reviewpage.html',{})                                              

class reviewView(View):
    def get(self, request):
        return render(request, 'review.html',{})                   

class reviewPageFlashcardView(View):
    def get(self, request):
        return render(request, 'reviewPageFlashcard.html', {})
        
class createquiz2View(View):
    def get(self, request):
        return render(request, 'createquiz2.html',{})   
      
class trueorfalsequestionView(View):
    def get(self, request):
        return render(request, 'trueorfalsequestion.html',{})   
class randompickerView(View):
    def get(self, request):
        return render(request, 'randompicker.html',{})        


class registerView(View):
    def get(self, request):
        form = UserForm()
        return render(request, 'register.html', {'form':form})

    def post(self, request):
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('App:login_view')
        return render(request, 'register.html', {'form':form})

#Apply mixins later
class createQuizView(View):
    def get(self, request):
        return render(request, 'createquiz.html',{})
        
class userView(View):
    def get(self, request):
        user = User.objects.all()
        quiz = Quiz.objects.all()
        classroom = Classroom.objects.all()
        context = {
            'user' : user,
            'quiz' : quiz,
            'classroom' : classroom
        }
        return render(request, 'user.html', context)
    
    def post(self, request):
        if request.method == 'POST':
            if 'userDelete' in request.POST: 
                userID = request.POST.get("userID")
                roomDelete = User.objects.filter(userID = userID).delete()
                print('recorded deleted')
            elif 'userUpdate' in request.POST: 
                userID = request.POST.get("userID")
                firstname = request.POST.get("firstname")
                lastname = request.POST.get("lastname") 
                phone_number = request.POST.get("phone_number")
                email = request.POST.get("email")
                agentUpdate = User.objects.filter(userID = userID).update(firstname = firstname, lastname = lastname, phone_number = phone_number, email = email)
            elif 'classroomDelete' in request.POST:
                roomID = request.POST.get("roomID")
                roomDelete = Classroom.objects.filter(roomID = roomID).delete()
                print('recorded deleted')
            elif 'classroomUpdate' in request.POST: 
                roomID = request.POST.get("roomID")
                status = request.POST.get("status")
                teacher = request.POST.get("teacher") 
                student = request.POST.get("student")
                classroomUpdate = Classroom.objects.filter(roomID = roomID).update(status = status, teacher = teacher, student = student)
            elif 'quizDelete' in request.POST:
                quiID = request.POST.get("quiID")
                quizDelete = Quiz.objects.filter(quiID = quiID).delete()
                print('recorded deleted')   
            elif 'quizUpdate' in request.POST: 
                quiID = request.POST.get("quiID")
                question = request.POST.get("question")
                quiztype = request.POST.get("quiztype") 
                subject = request.POST.get("subject")
                teacherID = request.POST.get("teacherID")
                answerOne = request.POST.get("answerOne")
                answerTwo = request.POST.get("answerTwo")
                answerThree = request.POST.get("answerThree")
                answerFour = request.POST.get("answerFour")
                quizUpdate = Quiz.objects.filter(quiID = quiID).update(question = question, quiztype = quiztype, subject = subject, teacherID = teacherID, answerOne = answerOne, answerTwo = answerTwo, answerThree = answerThree, answerFour = answerFour)         
        return redirect('App:user_view')     