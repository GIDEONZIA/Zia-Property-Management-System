# Generated by Django 5.2.3 on 2025-06-29 16:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='property',
            name='is_featured',
            field=models.BooleanField(default=False),
        ),
    ]
