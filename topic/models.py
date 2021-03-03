"""
Topic Models
"""
###
# Libraries
###
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext as _
from helpers.models import TimestampModel


###
# Choices
###


###
# Querysets
###


###
# Models
###
class Publishable(TimestampModel):
    """An abstract base model to support the creation
    of concrete publishable models (e.g.: topic).

    Inherits fields `created_at` and `updated_at` from
    `TimestampModel`.
    """
    title = models.CharField(
        verbose_name=_('title'),
        max_length=80
    )

    author = models.ForeignKey(
        to=get_user_model(),
        on_delete=models.CASCADE,
        verbose_name=_('author'),
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.title


class Topic(Publishable):
    """The model equivalent of a sub-reddit."""
    description = models.CharField(
        verbose_name=_('description'),
        max_length=140
    )

    url_name = models.SlugField(
        verbose_name=_('URL name'),
        max_length=30,
        unique=True
    )
