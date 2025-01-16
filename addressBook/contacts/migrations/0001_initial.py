# Generated by Django 5.0.4 on 2025-01-15 20:54

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(blank=True, max_length=255, null=True)),
                ('company_name', models.CharField(blank=True, max_length=255, null=True)),
                ('address', models.TextField(blank=True, null=True)),
                ('company_phone', models.CharField(blank=True, max_length=10, null=True)),
                ('email', models.EmailField(blank=True, help_text='Enter a valid email address', max_length=254, null=True)),
                ('fax_number', models.CharField(blank=True, max_length=100, null=True)),
                ('phone_number', models.CharField(blank=True, help_text='089999999', max_length=15, null=True, unique=True, validators=[django.core.validators.RegexValidator(message='Please correct valid phone number', regex='^(\\+359|0)?8[789]\\d{7}$')])),
                ('comment', models.TextField(blank=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contacts', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
