from django.contrib import messages
from django.shortcuts import render, redirect

# Create your views here.
from rest_framework.views import APIView
from .models import User
from django.contrib.auth.hashers import make_password
from django.contrib import auth
from django.db import IntegrityError

class Join(APIView):
    def get(self, request):
        return render(request, 'user/join.html')

    def post(self, request):
        if request.POST['password1'] == request.POST['password2']:
            try:
                User.objects.create(
                    email=request.POST['email'],
                    nickname=request.POST['nickname'],
                    name=request.POST['name'],
                    password=make_password(request.POST['password1']),
                    profile_image='../static/img/default_profile.png',
                    points=0
                )
                messages.add_message(self.request, messages.SUCCESS, '회원가입이 완료되었습니다.')
                return render(request, 'user/login.html')
            except IntegrityError as e:
                print(e)
                if str(e) == 'UNIQUE constraint failed: User.nickname':
                    messages.add_message(self.request, messages.ERROR, '이미 존재하는 닉네임입니다.')
                elif str(e) == 'UNIQUE constraint failed: User.email':
                    messages.add_message(self.request, messages.ERROR, '이미 존재하는 이메일입니다.')
                return render(request, 'user/join.html')

        messages.add_message(self.request, messages.ERROR, '비밀번호가 다릅니다.')
        return render(request, 'user/join.html')

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
