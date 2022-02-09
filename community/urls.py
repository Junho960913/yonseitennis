from django.urls import path, include
from .views import Board, Board_write, Board_detail, Board_delete, Board_modify
from django.conf import settings
from django.conf.urls.static import static

app_name = 'community'

urlpatterns = [
    path('board', Board.as_view()),
    path('board_write', Board_write.as_view()),
    path('board_detail/<int:pk>/', Board_detail.as_view()),
    path('board_detail/<int:pk>/delete/', Board_delete),
    path('board_detail/<int:pk>/modify/', Board_modify)
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
