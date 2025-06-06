# Generated by Django 5.1.6 on 2025-04-09 07:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0006_remove_land_name_land_property_property_owner_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='property',
            name='name',
        ),
        migrations.AddField(
            model_name='property',
            name='parent_property',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='child_properties', to='properties.property'),
        ),
    ]
