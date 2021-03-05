"""
Topic app's views
"""
###
# Libraries
###
from rest_framework.viewsets import ModelViewSet
from topic.api.serializers import TopicSerializer
from rest_framework.filters import OrderingFilter
from helpers.permissions import ObjectPermissionIsAuthenticatedOrReadOnly

###
# Viewsets
###
class TopicViewSet(ModelViewSet):
    """A basic viewset for the `Topic` model."""
    serializer_class = TopicSerializer
    model = TopicSerializer.Meta.model
    queryset = model.objects.all()
    lookup_field = 'url_name'
    filter_backends = [OrderingFilter]
    ordering = 'id'
    permission_classes = [ObjectPermissionIsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
