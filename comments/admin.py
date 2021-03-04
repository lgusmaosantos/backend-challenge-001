"""
Admin model registration
"""
###
# Libraries
###
from django.contrib import admin
from .models import Comment


###
# Models' registration
###
@admin.register(Comment)
class CommentModelAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'author',
        'post',
        'created_at',
        'updated_at'
    ]
    ordering = ['-updated_at']
