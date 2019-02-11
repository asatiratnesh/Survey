# Generated by Django 2.1.5 on 2019-02-05 10:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0003_organization_questions_library_survey_survey_quesmap'),
    ]

    operations = [
        migrations.CreateModel(
            name='ques_choices',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('choice', models.CharField(max_length=256)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('questions', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='survey.Questions_library')),
            ],
        ),
    ]
