from django.shortcuts import render, redirect

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import auth

class Join(APIView):
    def get(self, request):
        return render(request, 'user/join.html')

    def post(self, request):
        if request.POST['password1'] == request.POST['password2']:
            User.objects.create(
                email=request.POST['email'],
                nickname=request.POST['nickname'],
                name=request.POST['name'],
                password=make_password(request.POST['password1']),
                profile_image='../static/img/default_profile.png',
                points=0
            )
            return render(request, 'user/login.html', context=dict(message='회원가입이 완료되었습니다.'))

        return render(request, 'user/join.html', context=dict(message='회원가입에 실패하셨습니다.'))

class Login(APIView):
    def get(self, request):
        return render(request, 'user/login.html')

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = auth.authenticate(request, email=email, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            return render(request, 'user/login.html')


class Logout(APIView):
    def get(self, request):
        auth.logout(request)
        response = redirect('/')
        response.delete_cookie('hitboard')
        return response
