from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from .models import User
from django.shortcuts import redirect


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(username=username, password=password)
        if user is not None:
            print('인증 성공')
            login(request, user)
        else:
            print('인증 실패')
    return render(request, 'users/login.html')


def logout_view(request):
    logout(request)
    return redirect('users:login')

def signup_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        
        User.objects.create_user(username, email, password)
    return render(request, 'users/login.html')

def mainPage_view(request):
    return redirect('home')

