"""
Survey app url's
"""

from django.urls import path
from django.conf.urls import url
from django.contrib.auth import views as auth_views
from survey import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', auth_views.LoginView.as_view(template_name='survey/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='survey/logged_out.html'),
         name='logout'),
    path('signup/', views.signup, name='signup'),
    path('assignOrganization/', views.assign_organization, name='assign_organization'),
    path('organization/', views.organization, name='organization'),
    path('updateOrg/', views.update_org, name='updateOrg'),
    url(r'^(?P<org_id>[0-9]+)/deleteOrg/$', views.delete_org, name='deleteOrg'),
    path('emplList/', views.empl_list, name='emplList'),
    url(r'^(?P<empl_id>[0-9]+)/updateEmpl/$', views.update_empl, name='updateEmpl'),
    url(r'^(?P<empl_id>[0-9]+)/editEmpl/$', views.edit_empl, name='editEmpl'),
    url(r'^(?P<empl_id>[0-9]+)/deleteEmpl/$', views.delete_empl, name='deleteEmpl'),
    # path('profile/', views.update_profile, name='profile'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
    url(r'^questList', views.quest_list, name='questList'),
    url(r'^addQuest', views.AddQuest.as_view(), name='addQuest'),
    path('saveQuest/', views.save_quest, name='saveQuest'),
    path('updateQuest/', views.update_quest, name='updateQuest'),
    url(r'^(?P<quest_id>[0-9]+)/delete_question/$', views.delete_question, name='deleteQuestion'),
    path('surveyList', views.survey_list, name='surveyList'),
    url(r'^addSurvey', views.add_survey, name='addSurvey'),
    path('saveSurvey/', views.save_survey, name='saveSurvey'),
    url(r'^(?P<survey_id>[0-9]+)/surveyQuest/$', views.survey_quest, name='surveyQuest'),
    url(r'^(?P<survey_id>[0-9]+)/assignSurvey/$', views.assign_survey, name='assignSurvey'),
    url(r'^(?P<survey_id>[0-9]+)/deleteSurvey/$', views.delete_survey, name='deleteSurvey'),
    path('saveAssignSurvey/', views.save_assign_survey, name='saveAssignSurvey'),
    path('surveyListEmployee', views.survey_list_employee, name='surveyListEmployee'),
    url(r'(?P<survey_id>[0-9]+)/surveyQuestEmployee/$', views.survey_quest_employee,
        name='surveyQuestEmployee'),
    url(r'(?P<survey_id>[0-9]+)/saveSurveyAnswers/$', views.save_survey_answers,
        name='saveSurveyAnswers'),
    url(r'(?P<survey_id>[0-9]+)/surveyQuestResultEmployee/$', views.survey_quest_result_employee,
        name='surveyQuestResultEmployee'),
    url(r'^uploadEmplCSV/$', views.upload_empl_csv, name='uploadEmplCSV'),

    url(r'^reports/$', views.reports, name='reports'),
]
