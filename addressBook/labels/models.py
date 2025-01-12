from django.db import models

class Label(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True
    )

    color = models.CharField(max_length=100)

    profile = models.ForeignKey(
        'users.Profile',
        on_delete=models.CASCADE,
        related_name='labels'
    )

    def __str__(self):
        return self.name