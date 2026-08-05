# posts/admin.py
from django.contrib import admin

from .models import Author, Post

# Register your models here.
# Post model
admin.site.register(Post)
# Author model
admin.site.register(Author)
