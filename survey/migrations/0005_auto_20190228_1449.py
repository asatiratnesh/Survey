# Generated by Django 2.1.7 on 2019-02-28 09:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0004_auto_20190228_1442'),
    ]

    operations = [
        migrations.AlterField(
            model_name='survey',
            name='e_date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='survey',
            name='s_date',
            field=models.DateField(),
        ),
    ]
