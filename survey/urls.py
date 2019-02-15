from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf.urls import url
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('home/', views.index, name='index'),
    path('', auth_views.LoginView.as_view(template_name='survey/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='survey/logged_out.html'), name='logout'),
    path('signup/', views.signup, name='signup'),
    path('organization/', views.organization, name='organization'),

    # path('profile/', views.update_profile, name='profile'),
    path('profile/', views.update_profile, name='profile'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
    url(r'^questList', views.questList, name='questList'),
    url(r'^addQuest', views.AddQuest.as_view(), name='addQuest'),
    path('saveQuest/', views.saveQuest, name='saveQuest'),
    url(r'^(?P<quest_id>[0-9]+)/delete_question/$', views.deleteQuestion, name='deleteQuestion'),
    path('surveyList', views.surveyList, name='surveyList'),
    url(r'^addSurvey', views.addSurvey, name='addSurvey'),
    path('saveSurvey/', views.saveSurvey, name='saveSurvey'),
    url(r'^(?P<survey_id>[0-9]+)/surveyQuest/$', views.surveyQuest, name='surveyQuest'),
    url(r'^(?P<survey_id>[0-9]+)/assignSurvey/$', views.assignSurvey, name='assignSurvey'),
    url(r'^(?P<survey_id>[0-9]+)/deleteSurvey/$', views.deleteSurvey, name='deleteSurvey'),
    path('saveAssignSurvey/', views.saveAssignSurvey, name='saveAssignSurvey'),

    path('surveyListEmployee', views.surveyListEmployee, name='surveyListEmployee'),
    url(r'(?P<survey_id>[0-9]+)/surveyQuestEmployee/$', views.surveyQuestEmployee, name='surveyQuestEmployee'),
    url(r'(?P<survey_id>[0-9]+)/saveSurveyAnswers/$', views.saveSurveyAnswers, name='saveSurveyAnswers'),
    url(r'(?P<survey_id>[0-9]+)/surveyQuestResultEmployee/$', views.surveyQuestResultEmployee, name='surveyQuestResultEmployee'),

    url(r'^(?P<org_id>[0-9]+)/deleteOrg/$', views.deleteOrg, name='deleteOrg'),

]
