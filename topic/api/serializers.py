"""
Topic app's serializers
"""
###
# Libraries
###
from rest_framework import serializers
from rest_auth.serializers import UserDetailsSerializer
from ..models import Topic


###
# Serializers
###
class TopicSerializer(serializers.ModelSerializer):
    """A basic serializer for the `Topic` model."""
    author = UserDetailsSerializer(read_only=True)

    class Meta:
        model = Topic
        fields = [
            'id',
            'title',
            'author',
            'description',
            'url_name',
            'created_at',
            'updated_at'
        ]
