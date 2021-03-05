"""
API V1: Accounts Urls
"""
###
# Libraries
###
from django.conf.urls import include, url
from rest_framework import urlpatterns
from rest_framework.routers import SimpleRouter
from .views import TopicViewSet


###
# Routers
###
router = SimpleRouter()
router.register('topics', TopicViewSet)

###
# URLs
###
urlpatterns = [
    # Topic records
    url(r'^', include(router.urls))
]
