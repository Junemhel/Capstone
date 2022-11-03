from django.urls import include, path
from . import views
from django.contrib.auth import views as auth_view


app_name = 'App'
urlpatterns = [
    path('home', views.homeView.as_view(), name="home_view"),  
    path('about', views.aboutView.as_view(), name="about_view"),         
    path('contact', views.contactView.as_view(), name="contact_view"),
    path('login', auth_view.LoginView.as_view(template_name='login.html'),name="login_view"),
    path('register', views.registerView.as_view(), name="register_view"),   
    path('createquiz', views.createQuizView.as_view(), name="createQuiz_view"), 
    path('createclassadmin', views.createClassAdminView.as_view(), name="createClassAdmin_view"), 
    path('createclassteacher', views.createClassTeacherView.as_view(), name="createClassTeacher_view"), 
    path('createquiz2', views.createquiz2View.as_view(), name="createquiz2_view"),  
    path('trueorfalsequestion', views.trueorfalsequestionView.as_view(), name="trueorfalsequestion_view"),
    path('autogenerate', views.autoGenerateView.as_view(), name="autogenerate_view"),  
    path('reviewpage', views.reviewPageView.as_view(), name="reviewpage_view"), 
    path('reviewPageFlashcard', views.reviewPageFlashcardView.as_view(), name="reviewpageflashcard_view"), 
    path('review', views.reviewView.as_view(), name="review_view"),  
    path('user', views.userView.as_view(), name="user_view"),
    path('randompicker', views.randompickerView.as_view(), name="randompicker_view"),
    path('teacherdashboard', views.teacherdashboardView.as_view(), name="teacherdashboard_view"),
    path('studentdashboard', views.studentdashboardView.as_view(), name="studentdashboard_view"),
    path('teachers/', include(([
        path('', views.QuizListView.as_view(), name='quiz_change_list'),
        path('quiz/add/', views.QuizCreateView.as_view(), name='quiz_add'),
        path('quiz/<int:pk>/', views.QuizUpdateView.as_view(), name='quiz_change'),
        path('quiz/<int:pk>/delete/', views.QuizDeleteView.as_view(), name='quiz_delete'),
        path('quiz/<int:pk>/results/', views.QuizResultsView.as_view(), name='quiz_results'),
        path('quiz/<int:pk>/question/add/', views.question_add, name='question_add'),
        path('quiz/<int:quiz_pk>/question/<int:question_pk>/', views.question_change, name='question_change'),
        path('quiz/<int:quiz_pk>/question/<int:question_pk>/delete/', views.QuestionDeleteView.as_view(), name='question_delete'),
    ], 'classroom'), namespace='teachers')),
]    
    
   


