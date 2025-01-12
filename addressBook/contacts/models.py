from django.db import models

class Contact(models.Model):
    first_name = models.CharField(
        max_length=255
    )

    last_name = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    company_name = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    address = models.TextField(
        blank=True,
        null=True
    )

    company_phone = models.CharField(
        max_length=10,
        blank=True,
        null=True
    )

    email = models.EmailField(
        blank=True,
        null=True
    )

    fax_number = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    phone_number = models.CharField(
        max_length=10,
        blank=True,
        null=True
    )

    comment = models.TextField(
        blank=True,
        null=True
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
