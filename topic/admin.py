"""
Admin model registration
"""
###
# Libraries
###
from django.contrib import admin
from topic.models import Topic


###
# Models' registration
###
@admin.register(Topic)
class TopicModelAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'author',
        'created_at',
        'updated_at'
    ]
    ordering = ['-updated_at']
    prepopulated_fields = {
        'url_name': ('title',)
    }
