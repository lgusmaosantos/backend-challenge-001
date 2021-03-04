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
        'created_at',
        'updated_at'
    ]
    ordering = ['-updated_at']
