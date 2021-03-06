"""
Posts app's serializers
"""
###
# Libraries
###
from rest_framework import serializers
from rest_auth.serializers import UserDetailsSerializer
from ..models import Post


###
# Serializers
###
class PostSerializer(serializers.ModelSerializer):
    """A basic serializer for the `Post` model."""
    author = UserDetailsSerializer(read_only=True)
    topic = serializers.ReadOnlyField(source='topic.title')

    class Meta:
        model = Post
        fields = [
            'id',
            'title',
            'topic',
            'content',
            'created_at',
            'updated_at',
            'author'
        ]
