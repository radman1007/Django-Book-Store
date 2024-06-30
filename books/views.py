from .models import Book
from django.views import generic

class BookListView(generic.ListView):
    model = Book
    template_name = 'book_list.html'
    context_object_name = 'books'


class BookDetailView(generic.DetailView):
    model = Book
    template_name = 'book_detail.html'