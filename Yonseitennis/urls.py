"""Yonseitennis URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path, include

from .views import Sub, Profile, ProfileUpdate, NotificationDetail

app_name = 'Yonseitennis'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Sub.as_view()),
    path('profile/', Profile.as_view(), name='profile'),
    path('profile/update/', ProfileUpdate.as_view(), name='profile_update'),
    path('notification/<int:notification_pk>/match/<int:match_pk>',
         NotificationDetail.as_view(), name='notification-detail'),
    path('user/', include('user.urls')),
    path('content/', include('content.urls')),
    path('community/', include('community.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('match/', include('match.urls')),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
