from django.urls import path, include
from .views import Join, Login, Logout
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('join', Join.as_view(), name='join'),
    path('login', Login.as_view(), name='login'),
    path('logout', Logout.as_view(), name='logout')
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)