# Generated by Django 3.1.4 on 2021-01-08 21:12

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_merge_20210108_2315'),
    ]

    operations = [
        migrations.AlterField(
            model_name='complaint',
            name='date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
