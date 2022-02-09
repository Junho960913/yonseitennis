from django.db import models
from Yonseitennis import settings
from django.utils import timezone

# Create your models here.

class Match(models.Model):
    is_double = models.CharField(default='복식', max_length=10)
    sets = models.PositiveIntegerField(default=1)
    games = models.PositiveIntegerField(default=6)
    status = models.CharField(default='신청', max_length=10)
    team1_score = models.PositiveIntegerField(default=0)
    team2_score = models.PositiveIntegerField(default=0)
    player1_1 = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='player1_1', on_delete=models.CASCADE, null=True)
    player1_2 = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='player1_2', on_delete=models.CASCADE, null=True)
    player2_1 = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='player2_1', on_delete=models.CASCADE, null=True)
    player2_2 = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='player2_2', on_delete=models.CASCADE, null=True)

class Notification(models.Model):
    to_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='notification_to', on_delete=models.CASCADE, null=True)
    from_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='notification_from', on_delete=models.CASCADE, null=True)
    match = models.ForeignKey('Match', on_delete=models.CASCADE, related_name='match', blank=True, null=True)
    date = models.DateTimeField(default=timezone.now)
    user_has_seen = models.BooleanField(default=False)