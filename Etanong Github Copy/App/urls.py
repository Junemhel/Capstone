from django.urls import path
from . import views
from django.contrib.auth import views as auth_view


app_name = 'App'
urlpatterns = [ 
    path('home', views.homeView.as_view(), name="home_view"),  
    path('about', views.aboutView.as_view(), name="about_view"),         
    path('contact', views.contactView.as_view(), name="contact_view"),
    path('login', auth_view.LoginView.as_view(template_name='login.html'),name="login_view"),
    path('register', views.registerView.as_view(), name="register_view"),   
    path('createQuiz', views.createQuizView.as_view(), name="createQuiz_view"),  
    path('createquiz2', views.createquiz2View.as_view(), name="createquiz2_view"),  
    path('user', views.userView.as_view(), name="user_view"),
    path('choosetypeofquestion', views.choosetypeofquestionView.as_view(), name="choosetypeofquestion_view"),
     

    
   

]
