from django.shortcuts import render, redirect
from django.views.generic import View
from .forms import ContactForm
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.conf import settings

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, UpdateView

from django.db.models import Avg, Count, Q
from django.forms import inlineformset_factory
from itertools import chain

from .decorators import teacher_required, student_required
from .forms import BaseAnswerInlineFormSet, QuestionForm, TeacherSignUpForm, StudentInterestsForm, StudentSignUpForm, TakeQuizForm
from .models import Answer, Question, Quiz, User, Student, TakenQuiz

from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

# Create your views here.
from django.views.generic import TemplateView



class SignUpView(TemplateView):
    template_name = '2_signup.html'
# If user is authenticated = True, it checks if the user is a teacher and sends them to the quiz list html for teachers HTML
# else the user is a student and sends them to the quiz list html for students
# If the user isn't authenticated it redirects them to the home html
def home(request):
    if request.user.is_authenticated: 
        if request.user.is_teacher:
            return redirect('app:quiz_change_list')
        else:
            return redirect('app:quiz_list')
    return render(request, '1_home.html')


class HomeView(View):
    def get(self, request):
        if request.user.is_authenticated: 
            if request.user.is_teacher:
                return redirect('app:quiz_change_list')
            else:
                return redirect('app:quiz_list')        
        return render(request, '1_home.html', {})

class AboutView(View):
    def get(self, request):
        return render(request, '1_about.html',{})

class PickerView(View):
    def get(self, request):
        return render(request, '1_picker.html',{})    



class ContactView(View):
    def get(self, request):
        return render(request, '2_contact.html',{})

    def post(self,request):
        if request.method == "POST":
            
            email = request.POST['email']
            subject = request.POST['subject']
            
            message_header = "From: " + email + '\n'
            
            message_body_email = "Message: " + request.POST['message'] 
            message = message_header +  message_body_email   
            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                ['contactusetangong@gmail.com'],
                fail_silently=False,)
            return render(request, '2_contact.html',{})

# The view class associated when creating a teacher account
class TeacherSignUpView(CreateView):
    model = User
    form_class = TeacherSignUpForm
    template_name = '2_signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'teacher'
        return super().get_context_data(**kwargs)
        
# After creating the account they are then redirected to the homepage for teachers which is the quiz list
    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('app:quiz_change_list')


class StudentSignUpView(CreateView):
    model = User
    form_class = StudentSignUpForm
    template_name = '2_signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'student'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect("app:quiz_list") ########################################################################################## Change when you have the student side set up

# Requires a teacher account to be logged in
@method_decorator([login_required, teacher_required], name='dispatch')
class QuizListTeacherView(ListView):
    model = Quiz
    ordering = ('name', )
    context_object_name = 'quizzes'
    template_name = '3_quiz_change_list.html'

# Retrieves data of distinct # of users that have taken the quiz along with the # of questions
    def get_queryset(self):
        queryset = self.request.user.quizzes \
            .select_related('subject') \
            .annotate(questions_count=Count('questions', distinct=True)) \
            .annotate(taken_count=Count('taken_quizzes', distinct=True))
        return queryset













@method_decorator([login_required, teacher_required], name='dispatch')
class QuizCreateView(CreateView):
    model = Quiz
    fields = ('name', 'subject', )
    template_name = '3_quiz_add_form.html'

# Handles the creation of the quiz
    def form_valid(self, form):
        # Creates, but the quiz instance isn't saved yet
        quiz = form.save(commit=False)
        # Sets the value to the current user that is logged in 
        quiz.owner = self.request.user
        quiz.save()
        messages.success(self.request, 'The quiz was created with success! Go ahead and add some questions now.')
        #Redirects the user to the quiz editing page of the new quiz, this is possible by return the primary key of the newly created quiz
        return redirect('app:quiz_change', quiz.pk)


@method_decorator([login_required, teacher_required], name='dispatch')
class QuizUpdateView(UpdateView):
    model = Quiz
    fields = ('name', 'subject', )
    context_object_name = 'quiz'
    template_name = '3_quiz_change_form.html'

# returns the identitfied summary of each item in the query set
    def get_context_data(self, **kwargs):
        kwargs['questions'] = self.get_object().questions.annotate(answers_count=Count('answers'))
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        '''
        This method is an implicit object-level permission management
        This view will only match the ids of existing quizzes that belongs
        to the logged in user.
        '''
        return self.request.user.quizzes.all()

    def get_success_url(self):
        return reverse('app:quiz_change', kwargs={'pk': self.object.pk})

# Retrieves the nescessary data of a quiz and sends the user to the quiz delete page, 
@method_decorator([login_required, teacher_required], name='dispatch')
class QuizDeleteView(DeleteView):
    model = Quiz
    context_object_name = 'quiz'
    template_name = '3_quiz_delete_confirm.html'
    success_url = reverse_lazy('app:quiz_change_list')

    # Deletes the current quiz
    def delete(self, request, *args, **kwargs):
        quiz = self.get_object()
        messages.success(request, 'The quiz %s was deleted with success!' % quiz.name)
        return super().delete(request, *args, **kwargs)

    def get_queryset(self):
        return self.request.user.quizzes.all()


@method_decorator([login_required, teacher_required], name='dispatch')
class QuizResultsView(DetailView):
    model = Quiz
    context_object_name = 'quiz'
    template_name = '3_quiz_results.html'

    # Returns the average score, who took the quiz, their score, and the average score of the quiz overall 
    def get_context_data(self, **kwargs):
        quiz = self.get_object()
        taken_quizzes = quiz.taken_quizzes.select_related('student__user').order_by('-date')
        total_taken_quizzes = taken_quizzes.count()
        quiz_score = quiz.taken_quizzes.aggregate(average_score=Avg('score'))
        extra_context = {
            'taken_quizzes': taken_quizzes,
            'total_taken_quizzes': total_taken_quizzes,
            'quiz_score': quiz_score
        }
        kwargs.update(extra_context)
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        return self.request.user.quizzes.all()


@login_required
@teacher_required
def question_add(request, pk):
    # By filtering the quiz by the url keyword argument `pk` and
    # by the owner, which is the logged in user, we are protecting
    # this view at the object-level. Meaning only the owner of
    # quiz will be able to add questions to it.

    # calls the given model and get object from that if that object or model doesn't exist it raises a 404 error
    quiz = get_object_or_404(Quiz, pk=pk, owner=request.user)

    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.quiz = quiz
            question.save()
            messages.success(request, 'You may now add answers/options to the question.')
            return redirect('app:question_change', quiz.pk, question.pk)
    else:
        form = QuestionForm()

    return render(request, '3_question_add_form.html', {'quiz': quiz, 'form': form})


@login_required
@teacher_required
def question_change(request, quiz_pk, question_pk):
    # Simlar to the `question_add` view, this view is also managing
    # the permissions at object-level. By querying both `quiz` and
    # `question` we are making sure only the owner of the quiz can
    # change its details and also only questions that belongs to this
    # specific quiz can be changed via this url 
    quiz = get_object_or_404(Quiz, pk=quiz_pk, owner=request.user)
    question = get_object_or_404(Question, pk=question_pk, quiz=quiz)

    AnswerFormSet = inlineformset_factory(
        Question,  # parent model
        Answer,  # base model
        formset=BaseAnswerInlineFormSet,
        fields=('text', 'is_correct'),
        min_num=2,
        validate_min=True,
        max_num=10,
        validate_max=True
    )

    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)
        formset = AnswerFormSet(request.POST, instance=question)
        if form.is_valid() and formset.is_valid():
            with transaction.atomic():
                form.save()
                formset.save()
            messages.success(request, 'Question and answers saved with success!')
            return redirect('app:quiz_change', quiz.pk)
    else:
        form = QuestionForm(instance=question)
        formset = AnswerFormSet(instance=question)

    return render(request, '3_question_change_form.html', {
        'quiz': quiz,
        'question': question,
        'form': form,
        'formset': formset
    })


@method_decorator([login_required, teacher_required], name='dispatch')
class QuestionDeleteView(DeleteView):
    model = Question
    context_object_name = 'question'
    template_name = '3_question_delete_confirm.html'
    pk_url_kwarg = 'question_pk'

    def get_context_data(self, **kwargs):
        question = self.get_object()
        kwargs['quiz'] = question.quiz
        return super().get_context_data(**kwargs)

    def delete(self, request, *args, **kwargs):
        question = self.get_object()
        messages.success(request, 'The question %s was deleted with success!' % question.text)
        return super().delete(request, *args, **kwargs)

    def get_queryset(self):
        return Question.objects.filter(quiz__owner=self.request.user)

    def get_success_url(self):
        question = self.get_object()
        return reverse('app:quiz_change', kwargs={'pk': question.quiz_id})


#######################################################################################################################################
# Student Views                                                                                                                       # 
####################################################################################################################################### 



@method_decorator([login_required, student_required], name='dispatch')
class StudentInterestsView(UpdateView):
    model = Student
    form_class = StudentInterestsForm
    template_name = '4_interests_form.html'
    success_url = reverse_lazy('app:quiz_list')

    def get_object(self):
        return self.request.user.student

    def form_valid(self, form):
        messages.success(self.request, 'Interests updated with success!')
        return super().form_valid(form)


@method_decorator([login_required, student_required], name='dispatch')
class QuizListView(ListView):
    model = Quiz
    ordering = ('name', )
    context_object_name = 'quizzes'
    template_name = '4_quiz_list.html'

    def get_queryset(self):
        student = self.request.user.student
        student_interests = student.interests.values_list('pk', flat=True)
        taken_quizzes = student.quizzes.values_list('pk', flat=True)
        queryset = Quiz.objects.filter(subject__in=student_interests) \
            .exclude(pk__in=taken_quizzes) \
            .annotate(questions_count=Count('questions')) \
            .filter(questions_count__gt=0)
        return queryset


@method_decorator([login_required, student_required], name='dispatch')
class TakenQuizListView(ListView):
    model = TakenQuiz
    context_object_name = 'taken_quizzes'
    template_name = '4_taken_quiz_list.html'

    def get_queryset(self):
        queryset = self.request.user.student.taken_quizzes \
            .select_related('quiz', 'quiz__subject') \
            .order_by('quiz__name')
        return queryset


@login_required
@student_required
def take_quiz(request, pk):
    quiz = get_object_or_404(Quiz, pk=pk)
    student = request.user.student

    if student.quizzes.filter(pk=pk).exists():
        return render(request, '4_taken_quiz.html')

    total_questions = quiz.questions.count()
    unanswered_questions = student.get_unanswered_questions(quiz)
    total_unanswered_questions = unanswered_questions.count()
    progress = 100 - round(((total_unanswered_questions - 1) / total_questions) * 100)
    question = unanswered_questions.first()

    if request.method == 'POST':
        form = TakeQuizForm(question=question, data=request.POST)
        if form.is_valid():
            with transaction.atomic():
                student_answer = form.save(commit=False)
                student_answer.student = student
                student_answer.save()
                if student.get_unanswered_questions(quiz).exists():
                    return redirect('app:take_quiz', pk)
                else:
                    correct_answers = student.quiz_answers.filter(answer__question__quiz=quiz, answer__is_correct=True).count()
                    score = round((correct_answers / total_questions) * 100.0, 2)
                    TakenQuiz.objects.create(student=student, quiz=quiz, score=score)
                    if score < 50.0:
                        messages.warning(request, 'Better luck next time! Your score for the quiz %s was %s.' % (quiz.name, score))
                    else:
                        messages.success(request, 'Congratulations! You completed the quiz %s with success! You scored %s points.' % (quiz.name, score))
                    return redirect('app:quiz_list')
    else:
        form = TakeQuizForm(question=question)

    return render(request, '4_take_quiz_form.html', {
        'quiz': quiz,
        'question': question,
        'form': form,
        'progress': progress
    })

#######################################################################################################################################
# Logout                                                                                                                              # 
####################################################################################################################################### 
def logout_user(request):
    logout(request)
    messages.success(request, ("You Are Now Logged Out!"))
    return redirect('app:home_view')

def login_user(request, user):
    messages.success(request, ("You Are Now Logged In!"))
    login(request, user)
    
    return redirect('app:home_view')

#######################################################################################################################################
# Reviews                                                                                                                             # 
####################################################################################################################################### 


class ReviewView(View):
    def get(self, request):      
        return render(request, '5_review.html', {})

#  return Question.objects.filter(quiz__owner=self.request.user)
@login_required
@student_required
def review_quiz(request, pk):   #==================================REVIEW WORK=====================================#
    quiz = get_object_or_404(Quiz, pk=pk) #==================================REVIEW WORK=====================================#
    # student = request.user.student #==================================REVIEW WORK=====================================#
    # total_questions = quiz.questions.count() #==================================REVIEW WORK=====================================#
    # unanswered_questions = student.get_unanswered_questions(quiz) #==================================REVIEW WORK=====================================#
    # total_unanswered_questions = unanswered_questions.count() #==================================REVIEW WORK=====================================#
    # progress = 100 - round(((total_unanswered_questions - 1) / total_questions) * 100) #==================================REVIEW WORK=====================================#
    # question = unanswered_questions.first() #==================================REVIEW WORK=====================================#
   

    # question = get_object_or_404(Question, quiz=pk)

    # answer = get_object_or_404(Answer, Q(question=question.pk & is_correct=1))
    # question = Question.objects.filter(
    #     Q(quiz=pk)
    # )
    # answer = Answer.objects.filter(
    #     Q(question=question) & Q(is_correct=1)
    # )
    # flashcards = list(chain(question, answer))

    data = Answer.objects.filter(is_correct = 1)


    return render(request, '5_review.html', { 
        'data' : data,
        'quiz' : quiz
    })

