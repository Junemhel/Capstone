from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.forms.utils import ValidationError

from app.models import (Answer, Question, Student, StudentAnswer, Subject, User)

class ContactForm(forms.Form):
    name = forms.CharField(max_length = 255)
    email_address = forms.EmailField(max_length = 255)
    message = forms.CharField(widget = forms.Textarea(attrs={'rows':50, 'cols':6}), max_length = 2000, )

# the class that creates and saves a user as a teacher
class TeacherSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_teacher = True
        if commit:
            user.save()
        return user

# the class that creates and saves a user as a teacher
class TeacherSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_teacher = True
        if commit:
            user.save()
        return user

# The class that creates and saves a user as a student, it also has the option of letting the student select a subject of thier interest while registering
class StudentSignUpForm(UserCreationForm):
    interests = forms.ModelMultipleChoiceField(
        queryset=Subject.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

    class Meta(UserCreationForm.Meta):
        model = User
# If this block of code is successful, the changes are commited, if there is an exception the changes are rolledback
    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_student = True
        user.save()
        student = Student.objects.create(user=user)
        # cleaned data here returns a dictionary of validated inputs fields and their values 
        student.interests.add(*self.cleaned_data.get('interests'))
        return user

# This class is the list of subjects that the student can select if they are interested in them
class StudentInterestsForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ('interests', )
        widgets = {
            'interests': forms.CheckboxSelectMultiple
        }

# This is the class for creating the question forms, in which it calls the Question class in the models.py, and sets the entry to be a text field
class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('text', )

# Checks if the question has at least one forrect answer
class BaseAnswerInlineFormSet(forms.BaseInlineFormSet):
    def clean(self):
        super().clean()

        has_one_correct_answer = False
        for form in self.forms:
            if not form.cleaned_data.get('DELETE', False):
                if form.cleaned_data.get('is_correct', False):
                    has_one_correct_answer = True
                    break
        if not has_one_correct_answer:
            raise ValidationError('Mark at least one answer as correct.', code='no_correct_answer')

# This class is responsible for creating the quiz form where the student can answer the quiz, 
class TakeQuizForm(forms.ModelForm):
    answer = forms.ModelChoiceField(
        queryset=Answer.objects.none(),
        widget=forms.RadioSelect(),
        required=True,
        empty_label=None)

    class Meta:
        model = StudentAnswer
        fields = ('answer', )
# On initialization, if the question is in the dictionary is it returned and removed, then sets up the answer fields and ordered by ascending order (lowest value first) 
    def __init__(self, *args, **kwargs):
        question = kwargs.pop('question')
        super().__init__(*args, **kwargs)
        self.fields['answer'].queryset = question.answers.order_by('text')

