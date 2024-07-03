from .models import Book
from django.views import generic
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, render
from .forms import CommentForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.paginator import Paginator
from django.db.models import Q

def list_view(request):
    books = Book.objects.all()
    if request.method == 'POST':
        search_query = request.POST['search_query']
        books = Book.objects.filter(Q(author__icontains=search_query)|Q(title__icontains=search_query))
        context = {
            'books' : books,
            'page_obj' : page_obj,
            }
        return render(request, 'book_list.html', context)
    paginator = Paginator(books, 2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'books' : books,
        'page_obj' : page_obj,
    }
    return render(request, 'book_list.html', context)


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

    
class BookUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Book
    fields = ['title', 'author', 'description', 'price', 'cover']
    template_name = 'book_update.html'
    
    def test_func(self):
        obj = self.get_object()
        return obj.user == self.request.user
    
    
class BookDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Book
    template_name = 'book_delete.html'
    success_url = reverse_lazy('book_list')
    
    def test_func(self):
        obj = self.get_object()
        return obj.user == self.request.user