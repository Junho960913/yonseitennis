from datetime import timezone

from django.db.models import Q
from django.http import Http404
from django.shortcuts import render, redirect

# Create your views here.
from rest_framework.views import APIView
from django.views.generic import ListView, DetailView
from user.models import User
from .models import Match, Notification
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

class Rank(ListView):

    model = User
    template_name = 'match/rank.html'
    context_object_name = 'user'
    paginate_by = 10
    ordering = ['rank']

    def get_context_data(self, **kwargs):

        players = User.objects.order_by('-points')
        current_rank = 1
        counter = 0

        for player in players:
            if counter < 1:  # for first player
                player.rank = current_rank
            else:  # for other players
                if player.points == players[counter - 1].points:
                    # if player and previous player have same score,
                    # give them the same rank
                    player.rank = current_rank
                else:
                    # first update the rank
                    current_rank += 1
                    # then assign new rank to player
                    player.rank = current_rank
            counter += 1
            player.save()

        context = super(Rank, self).get_context_data(**kwargs)
        paginator = context['paginator']
        page_numbers_range = 5  # Display only 5 page numbers
        max_index = len(paginator.page_range)

        page = self.request.GET.get('page')
        current_page = int(page) if page else 1

        start_index = int((current_page - 1) / page_numbers_range) * page_numbers_range
        end_index = start_index + page_numbers_range
        if end_index >= max_index:
            end_index = max_index

        page_range = paginator.page_range[start_index:end_index]
        context['page_range'] = page_range
        return context




class Play(LoginRequiredMixin, ListView):
    login_url = '/user/login'
    template_name = 'match/play.html'
    context_object_name = 'match'
    paginate_by = 10

    def get_queryset(self):
        filtered = self.request.GET.get('filter', None)

        if filtered == '2':
            filtered_match = Match.objects.filter(
                Q(player1_1=self.request.user) |
                Q(player1_1=self.request.user) |
                Q(player2_1=self.request.user) |
                Q(player2_2=self.request.user),
                is_double='단식'
            ).order_by('-pk')

        elif filtered == '3':
            filtered_match = Match.objects.filter(
                Q(player1_1=self.request.user) |
                Q(player1_1=self.request.user) |
                Q(player2_1=self.request.user) |
                Q(player2_2=self.request.user),
                is_double='복식'
            ).order_by('-pk')

        elif filtered == '4':
            filtered_match = Match.objects.filter(
                Q(player1_1=self.request.user) |
                Q(player1_1=self.request.user) |
                Q(player2_1=self.request.user) |
                Q(player2_2=self.request.user),
                status='신청'
            ).order_by('-pk')

        elif filtered == '5':
            filtered_match = Match.objects.filter(
                Q(player1_1=self.request.user) |
                Q(player1_1=self.request.user) |
                Q(player2_1=self.request.user) |
                Q(player2_2=self.request.user),
                status='진행중'
            ).order_by('-pk')

        elif filtered == '6':
            filtered_match = Match.objects.filter(
                Q(player1_1=self.request.user) |
                Q(player1_1=self.request.user) |
                Q(player2_1=self.request.user) |
                Q(player2_2=self.request.user),
                status='경기종료'
            ).order_by('-pk')

        else:
            filtered_match = Match.objects.filter(
                Q(player1_1=self.request.user) |
                Q(player1_1=self.request.user) |
                Q(player2_1=self.request.user) |
                Q(player2_2=self.request.user),
            ).order_by('-pk')

        return filtered_match

    def get_context_data(self, **kwargs):
        context = super(Play, self).get_context_data(**kwargs)
        paginator = context['paginator']
        page_numbers_range = 5  # Display only 5 page numbers
        max_index = len(paginator.page_range)

        page = self.request.GET.get('page')
        current_page = int(page) if page else 1

        start_index = int((current_page - 1) / page_numbers_range) * page_numbers_range
        end_index = start_index + page_numbers_range
        if end_index >= max_index:
            end_index = max_index

        page_range = paginator.page_range[start_index:end_index]
        context['page_range'] = page_range
        users = User.objects.all()
        context['users'] = users
        context['filter'] = self.request.GET.get('filter', '진행중')
        return context


class Makematch(APIView):
    def post(self, request):
        player1_2 = request.POST.get('player1_2')
        print(player1_2)
        if player1_2 != 'none':
            player1_2 = User.objects.get(nickname=player1_2)
        else:
            player1_2 = None

        player2_1 = request.POST.get('player2_1')
        if player2_1 != 'none':
            player2_1 = User.objects.get(nickname=player2_1)
        else:
            player2_1 = None

        player2_2 = request.POST.get('player2_2')
        if player2_2 != 'none':
            player2_2 = User.objects.get(nickname=player2_2)
        else:
            player2_2 = None

        Match.objects.create(
            is_double=request.POST.get('is_double', '복식'),
            sets=request.POST.get('sets', 1),
            games=request.POST.get('games', 6),
            player1_1=request.user,
            player1_2=player1_2,
            player2_1=player2_1,
            player2_2=player2_2
        )

        Notification.objects.create(
            to_user=player2_1,
            from_user=request.user,
            match=Match.objects.last()
        )

        return redirect('/match/play')


class Admit(APIView):

    def post(self, request, match_pk, *args, **kwargs):
        match = Match.objects.get(pk=match_pk)
        if request.POST.get('reply') == 'yes':
            match.status = '진행중'
            match.save()
        elif request.POST.get('reply') == 'no':
            match.status = '거절'
            match.save()

        elif request.POST.get('reply') == 'cancel':
            match.status = '취소'
            match.save()

        notification = Notification.objects.get(match=match)
        if not notification.user_has_seen:
            notification.user_has_seen = True
            notification.save()
        return redirect('/match/play')


class Score(APIView):
    def post(self, request, match_pk):
        match = Match.objects.get(pk=match_pk)
        team1_score = request.POST.get('team_1')
        team2_score = request.POST.get('team_2')
        match.team1_score = team1_score
        match.team2_score = team2_score

        if match.status != '경기종료':
            match.status = '경기종료'
            match.save()

            if match.is_double == '단식':
                player1_1 = User.objects.get(nickname=match.player1_1)
                player2_1 = User.objects.get(nickname=match.player2_1)

                if team1_score > team2_score:
                    player1_1.points += 100

                else:
                    player2_1.points += 100

                player1_1.save()
                player2_1.save()

            else:
                player1_1 = User.objects.get(nickname=match.player1_1)
                player1_2 = User.objects.get(nickname=match.player1_2)
                player2_1 = User.objects.get(nickname=match.player2_1)
                player2_2 = User.objects.get(nickname=match.player2_2)

                if team1_score > team2_score:
                    player1_1.points += 100
                    player1_2.points += 100

                else:
                    player2_1.points += 100
                    player2_2.points += 100

                player1_1.save()
                player1_2.save()
                player2_1.save()
                player2_2.save()
        else:
            messages.add_message(self.request, messages.ERROR, '이미 종료된 게임입니다.')

        return redirect('/match/play')

