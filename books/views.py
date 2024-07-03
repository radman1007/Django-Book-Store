from .models import Book
from django.views import generic
from django.urls import reverse_lazy

class BookListView(generic.ListView):
    model = Book
    paginate_by = 3
    template_name = 'book_list.html'
    context_object_name = 'books'


class BookDetailView(generic.DetailView):
    model = Book
    template_name = 'book_detail.html'
    
    
class BookCreateView(generic.CreateView):
    model = Book
    fields = ['title', 'author', 'description', 'price', 'cover']
    template_name = 'book_create.html'
    
    
class BookUpdateView(generic.UpdateView):
    model = Book
    fields = ['title', 'author', 'description', 'price', 'cover']
    template_name = 'book_update.html'
    
    
class BookDeleteView(generic.DeleteView):
    model = Book
    template_name = 'book_delete.html'
    success_url = reverse_lazy('book_list')