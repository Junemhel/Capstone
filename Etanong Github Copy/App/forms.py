from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

class ClassroomForm(forms.ModelForm):
	class Meta:
		model = Classroom
		fields= '__all__'

class QuizForm(forms.ModelForm):
	class Meta:
		model = Quiz
		fields= '__all__'


class UserForm(UserCreationForm):
    firstname = forms.CharField(max_length= 100)
    lastname = forms.CharField(max_length= 100)
    phone_number = forms.CharField(max_length=11)
    email = forms.EmailField()
    class Meta:
        model = User
        fields =  ('firstname', 'lastname', 'phone_number', 'email', 'username', 'password1', 'password2' )