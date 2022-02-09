from django.urls import path, include
from .views import Introduce, Regulations
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('introduce', Introduce.as_view()),
    path('regulations', Regulations.as_view())
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)