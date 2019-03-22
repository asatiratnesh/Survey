from django.db import models
from django.contrib.auth.models import AbstractUser


# survey app models
class Organization(models.Model):
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class User(AbstractUser):
    is_org_admin = models.BooleanField(default=False)
    is_employee = models.BooleanField(default=False)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, null=True)


class Questions_library(models.Model):
    type = models.CharField(max_length=2)
    title = models.CharField(max_length=256)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = u'Questions_library'

    def __str__(self):
        return self.title


class ques_choices(models.Model):
    questions = models.ForeignKey(Questions_library, on_delete=models.CASCADE)
    choice = models.CharField(max_length=256)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.choice


class Survey(models.Model):
    name = models.CharField(max_length=200)
    s_date = models.DateField(null=True)
    e_date = models.DateField(null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Survey_QuesMap(models.Model):
    survey_id = models.ForeignKey(Survey, on_delete=models.CASCADE)
    question_id = models.ForeignKey(Questions_library, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
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
