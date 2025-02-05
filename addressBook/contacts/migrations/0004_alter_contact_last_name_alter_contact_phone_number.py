# Generated by Django 5.0.4 on 2025-01-19 20:07

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0003_alter_contact_image_alter_contact_labels'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='last_name',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='contact',
            name='phone_number',
            field=models.CharField(blank=True, help_text='08xxxxxxxx OR +3598xxxxxxxx', max_length=15, null=True, unique=True, validators=[django.core.validators.RegexValidator(message='Enter a valid phone number', regex='^(\\+359|0)?8[789]\\d{7}$')]),
        ),
    ]
