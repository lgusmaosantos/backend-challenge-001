"""
Posts app's views
"""
###
# Libraries
###
from rest_framework.viewsets import ModelViewSet
from posts.api.serializers import PostSerializer
from rest_framework.filters import OrderingFilter
from helpers.permissions import ObjectPermissionIsAuthenticatedOrReadOnly
from topic.models import Topic


###
# Viewsets
###
class PostViewSet(ModelViewSet):
    """A basic viewset for the `Post` model."""
    serializer_class = PostSerializer
    model = PostSerializer.Meta.model    
    filter_backends = [OrderingFilter]
    ordering = '-id'
    permission_classes = [ObjectPermissionIsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return self.model.objects.filter(
            topic__url_name=self.kwargs['topic_url_name']
        )

    def perform_create(self, serializer):
        topic = Topic.objects.get(url_name=self.kwargs['topic_url_name'])
        serializer.save(author=self.request.user, topic=topic)
