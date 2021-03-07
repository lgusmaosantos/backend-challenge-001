"""
backend-challenge-001 Nested Routers Setup
"""
###
# Libraries
###
from django.conf.urls import url, include
from rest_framework.routers import SimpleRouter
from rest_framework_nested.routers import NestedSimpleRouter
from topic.views import TopicViewSet
from posts.views import PostViewSet
from comments.views import CommentViewSet


###
# Routers
###
# Main router (`Topic` routes)
main_router = SimpleRouter()
main_router.register('topics', TopicViewSet)

# Post routes (nested on main router)
posts_router = NestedSimpleRouter(
    main_router,
    r'topics',
    lookup='topic'
)
posts_router.register(
    r'posts',
    PostViewSet,
    basename='post'
)

# Comment routes (nested on `posts_router`)
comments_router = NestedSimpleRouter(
    posts_router,
    r'posts',
    lookup='post'
)
comments_router.register(
    r'comments',
    CommentViewSet,
    basename='comment'
)
