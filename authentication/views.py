from django.shortcuts import render, redirect
from django.views import View
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from validate_email import validate_email
from django.contrib import messages
from django.contrib import auth

# Create your views here.

class EmailValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        email = data['email']
        if not validate_email(email):
            return JsonResponse({'email_error': 'Email is invalid'}, status=400)
        if User.objects.filter(email=email).exists():
            return JsonResponse({'email_error': 'sorry email in use,choose another one '}, status=409)
        return JsonResponse({'email_valid': True})

class UsernameValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        username = data['username']
        if not str(username).isalnum():
            return JsonResponse({'username_error': 'username should only contain alphanumeric characters'}, status=400)
        if User.objects.filter(username=username).exists():
            return JsonResponse({'username_error': 'sorry username in use,choose another one '}, status=409)
        return JsonResponse({'username_valid': True})


class RegistrationView(View):
    def get(self,request):
        return render(request,'authentica/register.html')
    
    def post(self,request):
       
       username=request.POST['username']
       email=request.POST['email']
       password=request.POST['password']

       context={
        'fieldValues': request.POST
       }
       if not User.objects.filter(username=username).exists():
           if not User.objects.filter(email=email).exists():

               if len(password)< 6:
                  messages.error(request,'password is too short')
                  return render(request,'authentica/register.html', context )
               user= User.objects.create_user(username=username, email=email)
               user.set_password(password)
               user.save()
               messages.success(request,'Account successfully created')
               return render(request,'authentica/register.html')

       return render(request,'authentica/register.html') 

class LoginView(View):
    def get(self, request):
        return render(request, 'authentica/login.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']

        if username and password:
            user = auth.authenticate(username=username, password=password)

            if user:
                if user.is_active:
                    auth.login(request, user)
                    messages.success(request, 'Welcome, ' +
                                     user.username+' its been a minute !')
                    return redirect('dashboard')
                else:
                    messages.error(request, 'Account is not active')
                return render(request, 'authentica/login.html')

            messages.error(
                request, 'Invalid credentials, register as new user instead ?')
            return render(request, 'authentica/login.html')

        messages.error(
            request, 'Please fill all fields')
        return render(request, 'authentica/login.html')


class LogoutView(View):
    def post(self, request):
        auth.logout(request)
        messages.success(request, 'You logged out')
        return redirect('login')