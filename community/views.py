from datetime import timezone

from django.http import Http404
from django.shortcuts import render, redirect

# Create your views here.
from rest_framework.views import APIView
from django.views.generic import ListView, DetailView, CreateView
from user.models import User
from .models import Contents
from .forms import Writing_contents
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from datetime import date, datetime, timedelta
from django.contrib.auth.mixins import LoginRequiredMixin

class Board(APIView, ListView):
    model = Contents
    template_name = 'community/board.html'
    context_object_name = 'contents'
    paginate_by = 10
    ordering = ['-id']

    def get_context_data(self, **kwargs):
        context = super(Board, self).get_context_data(**kwargs)
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
        email = self.request.session.get('email', None)
        user = User.objects.filter(email=email).first()
        context['user'] = user
        return context


class Board_write(LoginRequiredMixin, CreateView):
    login_url = '/user/login'
    def get(self, request):
        form = Writing_contents()
        return render(request, 'community/board_write.html', context=dict(form=form))

    def post(self, request):
        form = Writing_contents(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('/community/board')
        else:
            return redirect('/community/board_write')


class Board_detail(LoginRequiredMixin, DetailView):
    login_url = '/user/login'
    def get(self, request, pk):
        try:
            email = request.session.get('email', None)
            user = User.objects.filter(email=email).first()
            content = Contents.objects.get(pk=pk)
        except Contents.DoesNotExist:
            raise Http404('content does not exist')

        response = render(request, 'community/board_detail.html', context=dict(user=user, content=content))
        expire_date, now = datetime.now(), datetime.now()
        expire_date += timedelta(days=1)
        expire_date = expire_date.replace(hour=0, minute=0, second=0, microsecond=0)
        expire_date -= now
        max_age = expire_date.total_seconds()

        cookie_value = request.COOKIES.get('hitboard', '_')

        if f'_{pk}_' not in cookie_value:
            cookie_value += f'{pk}_'
            response.set_cookie('hitboard', value=cookie_value, max_age=max_age, httponly=True)
            content.hits += 1
            content.save()
        return response



def Board_delete(request, pk):
    content = Contents.objects.get(pk=pk)
    content.delete()
    print('edf')
    return redirect('/community/board')


def Board_modify(request, pk):
    content = Contents.objects.get(pk=pk)
    if request.method == "GET":
        form = Writing_contents(instance=content)
        # content.title = request.POST['title']
        # content.body = request.POST['body']
        # content.date = timezone.now()
        # try:
        #     content.image = request.FILES['image']
        # except:
        #     content.image = None
        # content.save()
        return render(request, 'community/board_modify.html', context=dict(form=form))


    else:
        form = Writing_contents(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            content.제목 = post.제목
            content.내용 = post.내용
            content.save()
        return redirect('/community/board_detail/' + str(content.id) + '/', context=dict(content=content))

