# Generated by Django 5.1.1 on 2024-10-24 00:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('csg', '0007_remove_stiffenedplate_area_ls_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='plate',
            name='description',
            field=models.TextField(null=True),
        ),
    ]
