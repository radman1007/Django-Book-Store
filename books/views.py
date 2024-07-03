from .models import Book
from django.views import generic
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, render
from .forms import CommentForm
from django.contrib.auth.mixins import LoginRequiredMixin

class BookListView(generic.ListView):
    model = Book
    paginate_by = 2
    template_name = 'book_list.html'
    context_object_name = 'books'


def book_detail_view(request, pk):
    book = get_object_or_404(Book, pk=pk)
    comments = book.comments.all()
    if request.method=='POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.book = book
            new_comment.user = request.user
            new_comment.save()
            comment_form = CommentForm()
    else:
        comment_form = CommentForm()
    context = {
        'book' : book,
        'comments' : comments,
        'comment_form' : comment_form,
    }
    return render(request, 'book_detail.html', context)
    
    
class BookCreateView(LoginRequiredMixin, generic.CreateView):
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