# Generated by Django 3.2.4 on 2021-06-25 10:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vacciapp', '0002_rename_map_slot_addmap'),
    ]

    operations = [
        migrations.AlterField(
            model_name='slot',
            name='addMap',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
