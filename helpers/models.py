"""
Model helper
"""
###
# Libraries
###
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext as _


###
# Helpers
###
class TimestampModel(models.Model):
    '''
        Extend this model if you wish to have automatically updated
        created_at and updated_at fields.
    '''

    class Meta:
        abstract = True

    created_at = models.DateTimeField(null=False, blank=True, auto_now_add=True)
    updated_at = models.DateTimeField(null=False, blank=True, auto_now=True)


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
