from django.test import TestCase
from django_webtest import WebTest
from django.urls import reverse
from survey.views import isValidEmail
from .models import Organization, User, Questions_library, ques_choices, Survey, Survey_QuesMap, SurveyEmployeeMap, Survey_Result

class ModelsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Organization.objects.create(name='Harbinger')
        User.objects.create(password='Harbinger', is_superuser=False, username='testuser', email='ratnesh@gmail.com')
        Questions_library.objects.create(type='1', title='your age?')
        ques_choices.objects.create(questions=Questions_library.objects.get(id=1), choice='yes')
        Survey.objects.create(name='survey_1', s_date='2019-02-28', e_date='2019-03-28')
        Survey_QuesMap.objects.create(survey_id=Survey.objects.get(id=1), question_id=Questions_library.objects.get(id=1))
        SurveyEmployeeMap.objects.create(survey_id=Survey.objects.get(id=1), empl_id=User.objects.get(id=1))
        Survey_Result.objects.create(survey=Survey.objects.get(id=1), empl=User.objects.get(id=1), question=Questions_library.objects.get(id=1),
                                     answer='yes', answer_status=False)

    def test_organization_is_instance(self):
        organization = Organization.objects.get(id=1)
        self.assertIsInstance(organization, Organization)

    def test_organization_title_label(self):
        organization = Organization.objects.get(id=1)
        type_field = organization._meta.get_field('name').verbose_name
        self.assertEquals(type_field, 'name')

    def test_user_is_instance(self):
        user = User.objects.get(id=1)
        self.assertIsInstance(user, User)

    def test_user_title_label(self):
        user = User.objects.get(id=1)
        type_field = user._meta.get_field('username').verbose_name
        self.assertEquals(type_field, 'username')

    def test_organization_object_name_is_title(self):
        organization = Organization.objects.get(id=1)
        expected_object_name = organization.name
        self.assertEquals(expected_object_name, str(organization))

    def test_questions_library_is_instance(self):
        questions_library = Questions_library.objects.get(id=1)
        self.assertIsInstance(questions_library, Questions_library)

    def test_questions_library_title_label(self):
        questions_library = Questions_library.objects.get(id=1)
        type_field = questions_library._meta.get_field('type').verbose_name
        self.assertEquals(type_field, 'type')

    def test_questions_library_object_name_is_title(self):
        questions_library = Questions_library.objects.get(id=1)
        expected_object_name = questions_library.title
        self.assertEquals(expected_object_name, str(questions_library))

    def test_ques_choices_is_instance(self):
        ques_choice = ques_choices.objects.get(id=1)
        self.assertIsInstance(ques_choice, ques_choices)

    def test_ques_choices_title_label(self):
        ques_choice = ques_choices.objects.get(id=1)
        type_field = ques_choice._meta.get_field('choice').verbose_name
        self.assertEquals(type_field, 'choice')

    def test_ques_choices_object_name_is_title(self):
        ques_choice = ques_choices.objects.get(id=1)
        expected_object_name = ques_choice.choice
        self.assertEquals(expected_object_name, str(ques_choice))

    def test_survey_is_instance(self):
        survey = Survey.objects.get(id=1)
        self.assertIsInstance(survey, Survey)

    def test_survey_title_label(self):
        survey = Survey.objects.get(id=1)
        type_field = survey._meta.get_field('name').verbose_name
        self.assertEquals(type_field, 'name')

    def test_survey_object_name_is_title(self):
        survey = Survey.objects.get(id=1)
        expected_object_name = survey.name
        self.assertEquals(expected_object_name, str(survey))

    def test_survey_quesMap_is_instance(self):
        survey_ques_map = Survey_QuesMap.objects.get(id=1)
        self.assertIsInstance(survey_ques_map, Survey_QuesMap)

    def test_survey_quesMap_title_label(self):
        survey_ques_map = Survey_QuesMap.objects.get(id=1)
        type_field = survey_ques_map._meta.get_field('survey_id').verbose_name
        self.assertEquals(type_field, 'survey id')

    def test_survey_employee_map_is_instance(self):
        survey_employee_map = SurveyEmployeeMap.objects.get(id=1)
        self.assertIsInstance(survey_employee_map, SurveyEmployeeMap)

    def test_survey_quesMap_title_label(self):
        survey_employee_map = SurveyEmployeeMap.objects.get(id=1)
        type_field = survey_employee_map._meta.get_field('survey_id').verbose_name
        self.assertEquals(type_field, 'survey id')

    def test_survey_result_is_instance(self):
        survey_result = Survey_Result.objects.get(id=1)
        self.assertIsInstance(survey_result, Survey_Result)

    def test_survey_quesMap_title_label(self):
        survey_result = Survey_Result.objects.get(id=1)
        type_field = survey_result._meta.get_field('answer').verbose_name
        self.assertEquals(type_field, 'answer')



class ViewsTestCase(TestCase):

    def test_emailID(self):
        self.assertTrue(isValidEmail("ratnesh@gmail.com"))