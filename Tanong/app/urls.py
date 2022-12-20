from django.urls import include, path
from . import views
from django.contrib.auth import views as auth_view


app_name = 'app'
urlpatterns = [
    path('home', views.HomeView.as_view(), name="home_view"), 
    path('about', views.AboutView.as_view(), name="about_view"),
    path('contact', views.ContactView.as_view(), name="contact_view"),   
    path('picker', views.PickerView.as_view(), name="picker_view"),
    path('signup/teacher', views.TeacherSignUpView.as_view(), name='teacher_signup'), 
    path('signup/student', views.StudentSignUpView.as_view(), name='student_signup'),
    path('signup', views.SignUpView.as_view(), name='signup'),

    path('quiz/', views.QuizListTeacherView.as_view(), name='quiz_change_list'),
    path('quiz/add/', views.QuizCreateView.as_view(), name='quiz_add'),
    path('quiz/<int:pk>/', views.QuizUpdateView.as_view(), name='quiz_change'),
    path('quiz/<int:pk>/delete/', views.QuizDeleteView.as_view(), name='quiz_delete'),
    path('quiz/<int:pk>/results/', views.QuizResultsView.as_view(), name='quiz_results'),
    path('quiz/<int:pk>/question/add/', views.question_add, name='question_add'),
    path('quiz/<int:quiz_pk>/question/<int:question_pk>/', views.question_change, name='question_change'),
    path('quiz/<int:quiz_pk>/question/<int:question_pk>/delete/', views.QuestionDeleteView.as_view(), name='question_delete'),

    path('accounts/profile/', views.QuizListView.as_view(), name='quiz_list'),
    path('accounts/interests/', views.StudentInterestsView.as_view(), name='student_interests'),
    path('accounts/taken/', views.TakenQuizListView.as_view(), name='taken_quiz_list'),
    path('accounts/quiz/<int:pk>/', views.take_quiz, name='take_quiz'),    
    
    path('accounts/', include('django.contrib.auth.urls'), name="login"),
    path('accounts/loggedout', views.logout_user, name="logout"),


]