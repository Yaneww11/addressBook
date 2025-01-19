from django.core.validators import RegexValidator
from django.db import models

from addressBook import settings
from addressBook.labels.models import Label


class Contact(models.Model):
    first_name = models.CharField(
        max_length=255
    )

    last_name = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    image = models.ImageField(
        upload_to='contact-images/',
        blank=True,
        null=True,
        default='default-images/default-profile-image.png',
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
                message='Enter a valid phone number'
            )
        ],
        help_text='08xxxxxxxx OR +3598xxxxxxxx',
    )

    comment = models.TextField(
        blank=True,
        null=True
    )

    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='contacts'
    )

    labels = models.ManyToManyField(
        to=Label,
        related_name='contacts',
        blank=True,
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
