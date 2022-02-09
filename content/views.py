from django.shortcuts import render, redirect

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView
from user.models import User
from django.contrib.auth.hashers import make_password


class Introduce(APIView):
    def get(self, request):
        return render(request, 'content/introduce.html')


class Regulations(APIView):
    def get(self, request):
        return render(request, 'content/regulations.html')
