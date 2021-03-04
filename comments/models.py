"""
Comments app's models
"""
###
# Libraries
###
from django.db import models
from django.utils.translation import ugettext as _
from helpers.models import Publishable
from posts.models import Post


###
# Choices
###


###
# Querysets
###


###
# Models
###
class Comment(Publishable):
    """The model equivalent of a comment. A comment
    belongs to a specific `Post` and is created by
    an user (`Publishable.author`).
    """
    content = models.TextField(
        verbose_name=_('content'),
        max_length=1000
    )

    post = models.ForeignKey(
        to=Post,
        on_delete=models.CASCADE,
        verbose_name=_('post')
    )
