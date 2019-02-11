from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    organization = models.CharField(max_length=120, blank=True)
    location = models.CharField(max_length=50, blank=True)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


# survey app models
class Organization(models.Model):
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Questions_library(models.Model):
    TEXT = 'text'
    RADIO = 'radio'
    SELECT = 'select'
    SELECT_MULTIPLE = 'select-multiple'
    QUESTION_TYPES = (
        (TEXT, 'text'),
        (RADIO, 'radio'),
        (SELECT, 'select'),
        (SELECT_MULTIPLE, 'Select Multiple'),
         )
    type = models.CharField(max_length=200, choices=QUESTION_TYPES, default=TEXT)
    title = models.CharField(max_length=256)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = u'Questions_library'

    def __str__(self):
        return self.title


class ques_choices(models.Model):
    questions = models.ForeignKey(Questions_library, on_delete=models.CASCADE)
    choice = models.CharField(max_length=256)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.choice


class Survey(models.Model):
    name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Survey_QuesMap(models.Model):
    survey_id = models.ForeignKey(Survey, on_delete=models.CASCADE)
    question_id = models.ForeignKey(Questions_library, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class SurveyEmployeeMap(models.Model):
    survey_id = models.ForeignKey(Survey, on_delete=models.CASCADE)
    empl_id = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Survey_Result(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    empl = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Questions_library, on_delete=models.CASCADE)
    answer = models.CharField(max_length=256)
    answer_status = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.answer
