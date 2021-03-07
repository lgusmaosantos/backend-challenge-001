"""
Comment app's views
"""
###
# Libraries
###
from rest_framework.viewsets import ModelViewSet
from .api.serializers import CommentSerializer
from rest_framework.filters import OrderingFilter
from helpers.permissions import ObjectPermissionIsAuthenticatedOrReadOnly
from posts.models import Post


###
# Viewsets
###
class CommentViewSet(ModelViewSet):
    """A basic viewset for the `Comment` model."""
    serializer_class = CommentSerializer
    model = CommentSerializer.Meta.model
    filter_backends = [OrderingFilter]
    ordering = '-id'
    permission_classes = [ObjectPermissionIsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return self.model.objects.filter(
            post=self.kwargs['post_pk']
        )

    def perform_create(self, serializer):
        post = Post.objects.get(id=self.kwargs['post_pk'])
        serializer.save(
            author=self.request.user,
            post=post
        )
