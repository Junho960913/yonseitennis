from django.shortcuts import render, redirect
from rest_framework.views import APIView
from match.models import Match, Notification
from user.models import User
from .forms import CustomCsUserChangeForm
from django.contrib import messages


class Sub(APIView):
    def get(self, request):
        return render(request, 'Yonseitennis/Yonseitennis.html')

    def post(self, request):
        return render(request, 'Yonseitennis/Yonseitennis.html')


class Profile(APIView):
    def get(self, request):
        return render(request, 'Yonseitennis/profile.html')

    def post(self, request):
        user = User.objects.get(nickname=request.user)
        profile_image = request.FILES['profile_image']
        user.profile_image = profile_image
        user.save()
        return redirect('profile')


class ProfileUpdate(APIView):

    def get(self, request):
        user_change_form = CustomCsUserChangeForm(instance=request.user)
        return render(request, 'Yonseitennis/profile_update.html', {'user_change_form': user_change_form})

    def post(self, request):
        user_change_form = CustomCsUserChangeForm(request.POST, instance=request.user)

        if user_change_form.is_valid():
            user_change_form.save()
            messages.add_message(request, messages.SUCCESS, '정보수정이 완료되었습니다.')
            return redirect('profile')





class NotificationDetail(APIView):
    def get(self, request, notification_pk, match_pk, *arg, **kwargs):
        notification = Notification.objects.get(pk=notification_pk)
        match = Match.objects.get(pk=match_pk)
        print(match.is_double)
        notification.user_has_seen = True
        notification.save()

        return redirect('match:play')