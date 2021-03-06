"""
Comments app's serializers
"""
###
# Libraries
###
from rest_framework import serializers
from rest_auth.serializers import UserDetailsSerializer
from ..models import Comment


###
# Serializers
###
class CommentSerializer(serializers.ModelSerializer):
    """A basic serializer for the `Comment` model."""
    author = UserDetailsSerializer(read_only=True)
    post = serializers.ReadOnlyField(source='post.title')

    class Meta:
        model = Comment
        fields = [
            'id',
            'title',
            'content',
            'created_at',
            'updated_at',
            'post',
            'author',
        ]
