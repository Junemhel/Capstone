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

class aboutView(View):
    def get(self, request):
        return render(request, 'about.html',{})

class contactView(View):
    def get(self, request):
        return render(request, 'contact.html',{})

class loginView(View):
    def get(self, request):
        return render(request, 'login.html',{})

class choosetypeofquestionView(View):
    def get(self, request):
        return render(request, 'choosetypeofquestion.html',{})

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

        context = {
            'user' : user,
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
        return redirect('App:user_view')     