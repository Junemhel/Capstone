from django.shortcuts import render
from collections import namedtuple
from django.db.models.fields import EmailField
from django.http import Http404
from django.shortcuts import render, redirect
from django.views.generic import View
from django.http import HttpResponse
from .models import *
from .forms import *
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Avg, Count
from django.forms import inlineformset_factory
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from .decorators import teacher_required
from .forms import BaseAnswerInlineFormSet, QuestionForm, TeacherSignUpForm
from .models import Answer, Question, Quiz, User


from django.core.mail import send_mail 
from django.conf import settings
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

    def post(self,request):
        if request.method == "POST":
            
            email = request.POST['email']
            subject = request.POST['subject']
            
            message_header = "From: " + email + '\n'
            message_body_default = "This is an automated message feedback from the site.\n"
            message_body_email = "Message: " + request.POST['message'] 
            message = message_header + message_body_default + message_body_email   
            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                ['contactusetangong@gmail.com'],
                fail_silently=False,)
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

# # Quiz CRUD


# class TeacherSignUpView(CreateView):
#     model = User
#     form_class = TeacherSignUpForm
#     template_name = 'registration/signup_form.html'

#     def get_context_data(self, **kwargs):
#         kwargs['user_type'] = 'teacher'
#         return super().get_context_data(**kwargs)

#     def form_valid(self, form):
#         user = form.save()
#         login(self.request, user)
#         return redirect('teachers:quiz_change_list')


# @method_decorator([login_required, teacher_required], name='dispatch')
# class QuizListView(ListView):
#     model = Quiz
#     ordering = ('name', )
#     context_object_name = 'quizzes'
#     template_name = 'classroom/teachers/quiz_change_list.html'

#     def get_queryset(self):
#         queryset = self.request.user.quizzes \
#             .select_related('subject') \
#             .annotate(questions_count=Count('questions', distinct=True)) \
#             .annotate(taken_count=Count('taken_quizzes', distinct=True))
#         return queryset


# @method_decorator([login_required, teacher_required], name='dispatch')
# class QuizCreateView(CreateView):
#     model = Quiz
#     fields = ('name', 'subject', )
#     template_name = 'classroom/teachers/quiz_add_form.html'

#     def form_valid(self, form):
#         quiz = form.save(commit=False)
#         quiz.owner = self.request.user
#         quiz.save()
#         messages.success(self.request, 'The quiz was created with success! Go ahead and add some questions now.')
#         return redirect('teachers:quiz_change', quiz.pk)


# @method_decorator([login_required, teacher_required], name='dispatch')
# class QuizUpdateView(UpdateView):
#     model = Quiz
#     fields = ('name', 'subject', )
#     context_object_name = 'quiz'
#     template_name = 'classroom/teachers/quiz_change_form.html'

#     def get_context_data(self, **kwargs):
#         kwargs['questions'] = self.get_object().questions.annotate(answers_count=Count('answers'))
#         return super().get_context_data(**kwargs)

#     def get_queryset(self):
#         '''
#         This method is an implicit object-level permission management
#         This view will only match the ids of existing quizzes that belongs
#         to the logged in user.
#         '''
#         return self.request.user.quizzes.all()

#     def get_success_url(self):
#         return reverse('teachers:quiz_change', kwargs={'pk': self.object.pk})


# @method_decorator([login_required, teacher_required], name='dispatch')
# class QuizDeleteView(DeleteView):
#     model = Quiz
#     context_object_name = 'quiz'
#     template_name = 'classroom/teachers/quiz_delete_confirm.html'
#     success_url = reverse_lazy('teachers:quiz_change_list')

#     def delete(self, request, *args, **kwargs):
#         quiz = self.get_object()
#         messages.success(request, 'The quiz %s was deleted with success!' % quiz.name)
#         return super().delete(request, *args, **kwargs)

#     def get_queryset(self):
#         return self.request.user.quizzes.all()


# @method_decorator([login_required, teacher_required], name='dispatch')
# class QuizResultsView(DetailView):
#     model = Quiz
#     context_object_name = 'quiz'
#     template_name = 'classroom/teachers/quiz_results.html'

#     def get_context_data(self, **kwargs):
#         quiz = self.get_object()
#         taken_quizzes = quiz.taken_quizzes.select_related('student__user').order_by('-date')
#         total_taken_quizzes = taken_quizzes.count()
#         quiz_score = quiz.taken_quizzes.aggregate(average_score=Avg('score'))
#         extra_context = {
#             'taken_quizzes': taken_quizzes,
#             'total_taken_quizzes': total_taken_quizzes,
#             'quiz_score': quiz_score
#         }
#         kwargs.update(extra_context)
#         return super().get_context_data(**kwargs)

#     def get_queryset(self):
#         return self.request.user.quizzes.all()


# @login_required
# @teacher_required
# def question_add(request, pk):
#     # By filtering the quiz by the url keyword argument `pk` and
#     # by the owner, which is the logged in user, we are protecting
#     # this view at the object-level. Meaning only the owner of
#     # quiz will be able to add questions to it.
#     quiz = get_object_or_404(Quiz, pk=pk, owner=request.user)

#     if request.method == 'POST':
#         form = QuestionForm(request.POST)
#         if form.is_valid():
#             question = form.save(commit=False)
#             question.quiz = quiz
#             question.save()
#             messages.success(request, 'You may now add answers/options to the question.')
#             return redirect('teachers:question_change', quiz.pk, question.pk)
#     else:
#         form = QuestionForm()

#     return render(request, 'classroom/teachers/question_add_form.html', {'quiz': quiz, 'form': form})


# @login_required
# @teacher_required
# def question_change(request, quiz_pk, question_pk):
#     # Simlar to the `question_add` view, this view is also managing
#     # the permissions at object-level. By querying both `quiz` and
#     # `question` we are making sure only the owner of the quiz can
#     # change its details and also only questions that belongs to this
#     # specific quiz can be changed via this url (in cases where the
#     # user might have forged/player with the url params.
#     quiz = get_object_or_404(Quiz, pk=quiz_pk, owner=request.user)
#     question = get_object_or_404(Question, pk=question_pk, quiz=quiz)

#     AnswerFormSet = inlineformset_factory(
#         Question,  # parent model
#         Answer,  # base model
#         formset=BaseAnswerInlineFormSet,
#         fields=('text', 'is_correct'),
#         min_num=2,
#         validate_min=True,
#         max_num=10,
#         validate_max=True
#     )

#     if request.method == 'POST':
#         form = QuestionForm(request.POST, instance=question)
#         formset = AnswerFormSet(request.POST, instance=question)
#         if form.is_valid() and formset.is_valid():
#             with transaction.atomic():
#                 form.save()
#                 formset.save()
#             messages.success(request, 'Question and answers saved with success!')
#             return redirect('teachers:quiz_change', quiz.pk)
#     else:
#         form = QuestionForm(instance=question)
#         formset = AnswerFormSet(instance=question)

#     return render(request, 'classroom/teachers/question_change_form.html', {
#         'quiz': quiz,
#         'question': question,
#         'form': form,
#         'formset': formset
#     })


# @method_decorator([login_required, teacher_required], name='dispatch')
# class QuestionDeleteView(DeleteView):
#     model = Question
#     context_object_name = 'question'
#     template_name = 'classroom/teachers/question_delete_confirm.html'
#     pk_url_kwarg = 'question_pk'

#     def get_context_data(self, **kwargs):
#         question = self.get_object()
#         kwargs['quiz'] = question.quiz
#         return super().get_context_data(**kwargs)

#     def delete(self, request, *args, **kwargs):
#         question = self.get_object()
#         messages.success(request, 'The question %s was deleted with success!' % question.text)
#         return super().delete(request, *args, **kwargs)

#     def get_queryset(self):
#         return Question.objects.filter(quiz__owner=self.request.user)

#     def get_success_url(self):
#         question = self.get_object()
#         return reverse('teachers:quiz_change', kwargs={'pk': question.quiz_id})
