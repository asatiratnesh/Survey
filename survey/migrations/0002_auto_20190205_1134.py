# Generated by Django 2.1.5 on 2019-02-05 06:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='organization',
            field=models.CharField(blank=True, max_length=120),
        ),
    ]