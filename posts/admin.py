"""
Admin model registration
"""
###
# Libraries
###
from django.contrib import admin
from .models import Post


###
# Models' registration
###
@admin.register(Post)
class PostModelAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'author',
        'topic',
        'created_at',
        'updated_at'
    ]
    list_filter = ['topic']
    ordering = ['-updated_at']
