# Generated by Django 5.1.6 on 2025-04-09 09:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0009_owner_customuser_alter_property_owner'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='agricultural',
            name='property',
        ),
        migrations.RemoveField(
            model_name='apartment',
            name='property',
        ),
        migrations.RemoveField(
            model_name='beachland',
            name='property',
        ),
        migrations.RemoveField(
            model_name='commercial',
            name='property',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='groups',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='user_permissions',
        ),
        migrations.RemoveField(
            model_name='hotel',
            name='property',
        ),
        migrations.RemoveField(
            model_name='house',
            name='property',
        ),
        migrations.RemoveField(
            model_name='industrial',
            name='property',
        ),
        migrations.RemoveField(
            model_name='land',
            name='property',
        ),
        migrations.RemoveField(
            model_name='mixeduse',
            name='property',
        ),
        migrations.RemoveField(
            model_name='office',
            name='property',
        ),
        migrations.RemoveField(
            model_name='other',
            name='property',
        ),
        migrations.AlterField(
            model_name='property',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='properties.property'),
        ),
        migrations.RemoveField(
            model_name='resort',
            name='property',
        ),
        migrations.RemoveField(
            model_name='restaurant',
            name='property',
        ),
        migrations.DeleteModel(
            name='Retail',
        ),
        migrations.RemoveField(
            model_name='vacation',
            name='property',
        ),
        migrations.RemoveField(
            model_name='warehouse',
            name='property',
        ),
        migrations.AlterField(
            model_name='property',
            name='name',
            field=models.CharField(default='No name', max_length=255),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='property',
            name='property_type',
            field=models.CharField(max_length=20),
        ),
        migrations.DeleteModel(
            name='Agricultural',
        ),
        migrations.DeleteModel(
            name='Apartment',
        ),
        migrations.DeleteModel(
            name='BeachLand',
        ),
        migrations.DeleteModel(
            name='Commercial',
        ),
        migrations.DeleteModel(
            name='CustomUser',
        ),
        migrations.DeleteModel(
            name='Hotel',
        ),
        migrations.DeleteModel(
            name='House',
        ),
        migrations.DeleteModel(
            name='Industrial',
        ),
        migrations.DeleteModel(
            name='Land',
        ),
        migrations.DeleteModel(
            name='MixedUse',
        ),
        migrations.DeleteModel(
            name='Office',
        ),
        migrations.DeleteModel(
            name='Other',
        ),
        migrations.DeleteModel(
            name='Owner',
        ),
        migrations.DeleteModel(
            name='Resort',
        ),
        migrations.DeleteModel(
            name='Restaurant',
        ),
        migrations.DeleteModel(
            name='Vacation',
        ),
        migrations.DeleteModel(
            name='Warehouse',
        ),
    ]
