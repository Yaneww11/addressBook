from django.core.validators import RegexValidator
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
        null=True,
        help_text='Enter a valid email address',
    )

    fax_number = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    phone_number = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^(\+359|0)?8[789]\d{7}$',
                message='Please correct valid phone number'
            )
        ],
        help_text='089999999',
    )

    comment = models.TextField(
        blank=True,
        null=True
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
