from django.urls import path, include
from .views import Rank, Play, Makematch, Admit, Score
from django.conf import settings
from django.conf.urls.static import static

app_name = 'match'

urlpatterns = [
    path('rank', Rank.as_view()),
    path('play', Play.as_view(), name='play'),
    path('play/makematch', Makematch.as_view(), name='makematch'),
    path('play/<int:match_pk>', Admit.as_view(), name='admit'),
    path('play/score/<int:match_pk>', Score.as_view(), name='score')
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
