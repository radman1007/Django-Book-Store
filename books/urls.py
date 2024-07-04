from django.urls import path
from .views import list_view, book_detail_view, book_create_view, BookUpdateView, BookDeleteView

urlpatterns = [
    path('', list_view, name='book_list'),
    path('<int:pk>/', book_detail_view, name='book_detail'),
    path('new/', book_create_view, name='book_create'),
    path('<int:pk>/edit/', BookUpdateView.as_view(), name='book_update'),
    path('<int:pk>/delete/', BookDeleteView.as_view(), name='book_delete'),
]
