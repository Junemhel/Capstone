from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.html import escape, mark_safe
# Create your models here.

# Clasifies whether the user is a teacher or student
class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)


# Creates the subject tag 
class Subject(models.Model):
    name = models.CharField(max_length=30)
    color = models.CharField(max_length=7, default='#007bff')

# Sting representation of the model's object, it will refer to this model's "name" property
    def __str__(self):
        return self.name

    def get_html_badge(self):
        name = escape(self.name)
        color = escape(self.color)
        html = '<span class="badge badge-primary" style="background-color: %s">%s</span>' % (color, name)
        return mark_safe(html)

# Holds who owns the quiz, what it is called, and what subject it is in
class Quiz(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quizzes')
    name = models.CharField(max_length=255)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='quizzes')

    def __str__(self):
        return self.name

# Holds the Quiz ID so it knows where it belongs, and the text for the question
class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    text = models.CharField('Question', max_length=255)

    def __str__(self):
        return self.text

# Holds the Which question it belongs to, the choices, the text of the choices, and a boolean field that tells if it is correct or not
class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    text = models.CharField('Answer', max_length=255)
    is_correct = models.BooleanField('Correct answer', default=False)

    def __str__(self):
        return self.text


# Holds the ID of the user, The ID of the Quizes, and the ID of the Interests tags (subjects) 
class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    quizzes = models.ManyToManyField(Quiz, through='TakenQuiz')
    interests = models.ManyToManyField(Subject, related_name='interested_students')

# retrieves the quiz answers from the StudenAnswer model, then filters it their answer to the question, and grabs the data primary key of the answered to the question. 
    def get_unanswered_questions(self, quiz):
        answered_questions = self.quiz_answers \
            .filter(answer__question__quiz=quiz) \
            .values_list('answer__question__pk', flat=True)
        # A Variable that holds, the excluded primary keys of answered questions, orders it by lowest value first
        questions = quiz.questions.exclude(pk__in=answered_questions).order_by('text') 
        return questions

    def __str__(self):
        return self.user.username

# Holds the values for the student's ID, quiz ID, their score, and when they took it
class TakenQuiz(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='taken_quizzes')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='taken_quizzes')
    score = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)

# Holds the values for the IDs of the students who answered the quiz, and the ID of their answers 
class StudentAnswer(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='quiz_answers')
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='+')
