"""
backend-challenge-001 URL Configuration
"""
###
# Libraries
###
from django.conf.urls import url, include
from django.contrib import admin
from helpers.health_check_view import health_check
from .routers import (
    main_router,
    posts_router,
    comments_router
)

###
# URLs
###
urlpatterns = [
    # Admin
    url(r'^admin/', admin.site.urls),

    # Health Check
    url(r'health-check/$', health_check, name='health_check'),

    # Applications
    url(r'^', include('accounts.urls')),
    url(r'^', include(main_router.urls)),
    url(r'^', include(posts_router.urls)),
    url(r'^', include(comments_router.urls))
]
