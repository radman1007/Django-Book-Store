from .models import Book
from django.views import generic
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, render, redirect
from .forms import CommentForm, BookForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q

def list_view(request):
    books = Book.objects.all()
    if request.method == 'POST':
        search_query = request.POST['search_query']
        if len(search_query) >= 1:
            books = Book.objects.filter(Q(author__icontains=search_query)|Q(title__icontains=search_query))
            context = {
                'books' : books,
                'query' : search_query,
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
    

@login_required()
def book_create_view(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            new_book = form.save(commit=False)
            new_book.user = request.user
            new_book.save()
            comment_form = CommentForm()
            return redirect('home')
    form = BookForm()
    context = {
        'form' : form
    }
    return render(request, 'book_create.html', context)

    
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