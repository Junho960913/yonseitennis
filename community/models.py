from django.db import models
from django.contrib.auth import get_user_model
from Yonseitennis import settings
from ckeditor_uploader.fields import RichTextUploadingField
# Create your models here.


class Contents(models.Model):
    제목 = models.CharField(max_length=100)
    내용 = RichTextUploadingField()
    image = models.ImageField(blank=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    date = models.DateField(auto_now_add=True, null=True)
    hits = models.PositiveIntegerField(default=0)

