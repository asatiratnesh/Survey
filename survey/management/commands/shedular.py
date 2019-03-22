"""
notification
"""

import datetime
import logging
from django.core.management.base import BaseCommand
from django.core.mail import EmailMessage
from survey.models import SurveyEmployeeMap, User


class Command(BaseCommand):
    help = 'Type the help text here'

    def handle(self, *args, **options):
        self.email_notification_one_day_before()
        self.email_notification_on_start_date()
        self.email_notification_one_day_before_end_date()
        self.email_notification_after_end_date()

    @staticmethod
    def email_notification_one_day_before():
        upcoming = SurveyEmployeeMap.objects.filter(survey_id__s_date__contains=
                                                    datetime.date.today() + datetime.timedelta(days=2))
        for survey_data in upcoming:
            try:
                empl = User.objects.get(pk=survey_data.empl_id.id)
                subject = 'You have a new survey coming tomorrow.'
                body = "Hi {},\n\n".format(empl.username)
                body += "You have a new survey coming tomorrow.\n"
                body += "Please login to survey management and complete your survey.\n"
                email = EmailMessage(
                    subject, body, to=[empl.email]
                )
                email.send()
            except Exception as e:  # pylint: disable=invalid-name
                logging.exception(e)

    @staticmethod
    def email_notification_on_start_date():
        started = SurveyEmployeeMap.objects.filter(survey_id__s_date__contains=datetime.date.today())
        for survey_data in started:
            try:
                empl = User.objects.get(pk=survey_data.empl_id.id)
                subject = 'You have a new survey in your dashboard.'
                body = "Hello {},\n\n".format(empl.username)
                body += "You have a new survey in your dashboard.\n"
                body += "Please login to survey management and complete your survey.\n\n"
                body += "Thanks,\n{}".format("Employee Survey Department")
                email = EmailMessage(
                    subject, body, to=[empl.email]
                )
                email.send()
            except Exception as e:
                logging.exception(e)

    @staticmethod
    def email_notification_one_day_before_end_date():
        started = SurveyEmployeeMap.objects.filter(survey_id__e_date__contains=
                                                   datetime.date.today() + datetime.timedelta(days=1))
        for survey_data in started:
            try:
                empl = User.objects.get(pk=survey_data.empl_id.id)
                subject = 'Survey assigned to you ending tomorrow.'
                body = "Hello {},\n\n".format(empl.username)
                body += "Survey in your dashboard ending tomorrow.\n"
                body += "Please login to survey management and complete your survey.\n\n"
                body += "Thanks,\n{}".format("Employee Survey Department")
                email = EmailMessage(
                    subject, body, to=[empl.email]
                )
                email.send()
            except Exception as e:
                logging.exception(e)

    @staticmethod
    def email_notification_after_end_date():
        started = SurveyEmployeeMap.objects.filter(survey_id__e_date__contains=datetime.date.today())
        for survey_data in started:
            try:
                empl = User.objects.get(pk=survey_data.empl_id.id)
                subject = 'Survey assigned to you was ended.'
                body = "Hello {},\n\n ".format(empl.username)
                body += "Survey in your dashboard ended.\n"
                body += "Please login to survey management and complete your survey.\n\n"
                body += "Thanks,\n{}".format("Employee Survey Department")
                email = EmailMessage(
                    subject, body, to=[empl.email]
                )
                email.send()
            except Exception as e:
                logging.exception(e)
