from django.db import models

from addressBook import settings


class Label(models.Model):
    name = models.CharField(
        max_length=100,
    )

    color = models.CharField(max_length=7)


    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='labels',
        blank=True,
        null=True,
    )

    class Meta:
        unique_together = ('name', 'user')

    def __str__(self):
        return self.name

