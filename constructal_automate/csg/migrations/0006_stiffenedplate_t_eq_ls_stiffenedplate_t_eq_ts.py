# Generated by Django 5.1.1 on 2024-10-12 21:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('csg', '0005_stiffenedplate_area_ls_stiffenedplate_area_ts_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='stiffenedplate',
            name='t_eq_ls',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='stiffenedplate',
            name='t_eq_ts',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
    ]
