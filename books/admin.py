from django.contrib import admin
from .models import Book, Comment

class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'text', 'recommend', 'datetime_created')
    

admin.site.register(Book)
admin.site.register(Comment, CommentAdmin)