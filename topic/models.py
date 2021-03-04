"""
Topic Models
"""
###
# Libraries
###
from django.db import models
from django.utils.translation import ugettext as _
from helpers.models import Publishable


###
# Choices
###


###
# Querysets
###


###
# Models
###
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
