# Generated by Django 5.1.1 on 2024-10-12 20:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('csg', '0004_alter_stiffenedplate_h_s_alter_stiffenedplate_t_1_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='stiffenedplate',
            name='area_ls',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='stiffenedplate',
            name='area_ts',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='stiffenedplate',
            name='length_ls',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='stiffenedplate',
            name='length_ts',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
    ]
