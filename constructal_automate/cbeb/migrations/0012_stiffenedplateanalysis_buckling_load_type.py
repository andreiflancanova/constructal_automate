# Generated by Django 5.0.7 on 2024-08-09 15:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cbeb', '0011_rename_bucklingtype_bucklingloadtype'),
    ]

    operations = [
        migrations.AddField(
            model_name='stiffenedplateanalysis',
            name='buckling_load_type',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to='cbeb.bucklingloadtype'),
            preserve_default=False,
        ),
    ]
