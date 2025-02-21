from .views import RegistrationView,EmailValidationView, UsernameValidationView, LoginView, LogoutView
from django.urls import path
from django.views.decorators.csrf import csrf_exempt

urlpatterns=[
    path('validate-username', csrf_exempt(UsernameValidationView.as_view()),
         name="validate-username"),
    path('login', LoginView.as_view(), name="login"),
    path('validate-email', csrf_exempt(EmailValidationView.as_view()),
         name='validate_email'),
    path('logout', LogoutView.as_view(), name="logout"),
    path('register',RegistrationView.as_view(), name='register'),
   
]