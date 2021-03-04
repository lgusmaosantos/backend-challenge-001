"""
Posts app's models
"""
###
# Libraries
###
from django.db import models
from django.utils.translation import ugettext as _
from helpers.models import Publishable
from topic.models import Topic


###
# Choices
###


###
# Querysets
###


###
# Models
###
class Post(Publishable):
    """The model equivalent of a Reddit thread, a `Post`
    belongs to a specific `Topic` and is created by an
    user (field `Publishable.author`).
    """
    content = models.TextField(
        verbose_name=_('content'),
        max_length=1000
    )

    topic = models.ForeignKey(
        to=Topic,
        on_delete=models.CASCADE,
        verbose_name=_('topic')
    )
