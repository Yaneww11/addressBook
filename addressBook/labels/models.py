from django.db import models

from addressBook import settings


class Label(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True
    )

    color = models.CharField(max_length=100)

    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='labels'
    )

    def __str__(self):
        return self.name
