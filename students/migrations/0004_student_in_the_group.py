# Generated by Django 3.2.6 on 2021-09-17 11:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0002_group_main_teacher'),
        ('students', '0003_logger'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='in_the_group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='groups.group'),
        ),
    ]