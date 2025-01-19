# Generated by Django 5.0.4 on 2025-01-19 20:07

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='phone_number',
            field=models.CharField(blank=True, help_text='08xxxxxxxx OR +3598xxxxxxxx', max_length=15, null=True, unique=True, validators=[django.core.validators.RegexValidator(message='Please provide a valid phone number', regex='^(\\+359|0)?8[789]\\d{7}$')]),
        ),
    ]
