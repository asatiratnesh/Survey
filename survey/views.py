from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.generic import TemplateView, ListView, DeleteView
from .tokens import account_activation_token
from .models import Questions_library, ques_choices, Survey, Survey_QuesMap, SurveyEmployeeMap, Survey_Result, \
    Organization
from .forms import UserForm, SignupForm
from django.core.mail import EmailMessage
from . import models
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.http import QueryDict

User = get_user_model()


@login_required(login_url='login')
def index(request):
    return render(request, 'survey/index.html')


@user_passes_test(lambda u: u.is_superuser or u.is_org_admin)
@login_required(login_url='login')
def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        print(form)
        if form.is_valid():
            try:
                userObj = form.save(commit=False)
                userObj.is_active = True
                if request.user.is_superuser:
                    print("+++++++++++++++111111")
                    userObj.is_org_admin = True
                    print(get_object_or_404(Organization, pk=request.POST['organization']))
                    userObj.organization = get_object_or_404(Organization, pk=request.POST['organization'])
                elif request.user.is_org_admin:
                    userObj.is_employee = True
                    userObj.organization = request.user.organization
                userObj.save()

            except Exception as e:
                messages.error(request, 'Error!!!')
                print(e)
            return redirect('emplList')

    form = SignupForm()
    org_list = Organization.objects.all()
    return render(request, 'survey/signup.html', {'form': form, 'org_list': org_list})


@user_passes_test(lambda u: u.is_org_admin)
@login_required(login_url='login')
def uploadEmplCSV(request):
    try:
        csv_file = request.FILES["empl_csv"]
        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'File is not CSV type')
            return redirect('emplList')
        # if file is too large, return
        if csv_file.multiple_chunks():
            messages.error(request, "Uploaded file is too big (%.2f MB)." % (csv_file.size / (1000 * 1000),))
            return redirect('emplList')

        file_data = csv_file.read().decode("utf-8")
        lines = file_data.split("\r\n")
        formSubmitMsg = True
        # loop over the lines and save them in db. If error , store as string and then display
        for line in lines:
            fields = line.split(",")
            data_dict = {}
            data_dict["csrfmiddlewaretoken"] = request.POST['csrfmiddlewaretoken']
            data_dict["username"] = fields[0]
            data_dict["email"] = fields[1]
            data_dict["password1"] = fields[2]
            data_dict["password2"] = fields[2]

            qdict = QueryDict('', mutable=True)
            qdict.update(data_dict)
            form = SignupForm(qdict)
            if form.is_valid():
                userObj = form.save(commit=False)
                userObj.is_active = True
                userObj.is_employee = True
                userObj.organization = request.user.organization
                userObj.save()
                formSubmitMsg = True
            else:
                formSubmitMsg = False

        if formSubmitMsg:
            messages.error(request, 'Saved Successfully !')
        else:
            messages.error(request, 'username must be unique, password should be 8 character and strong!')
        return redirect('emplList')

    except Exception as e:
        print(e)
        messages.error(request, "Unable to upload file. ")
    return redirect('emplList')


@user_passes_test(lambda u: u.is_superuser or u.is_org_admin)
@login_required(login_url='login')
def emplList(request):
    if request.user.is_superuser:
        users = User.objects.filter(is_org_admin=True)
    else:
        users = User.objects.filter(organization=request.user.organization)
    return render(request, 'survey/employeesList.html', {'users': users})


@login_required(login_url='login')
def editEmpl(request, empl_id):
    user_info = User.objects.only('first_name', 'email').get(pk=empl_id)
    return render(request, 'survey/edit_employee.html', {"empl_id": empl_id, 'user_info': user_info})


@login_required(login_url='login')
def updateEmpl(request, empl_id):
    User.objects.filter(pk=empl_id).update(email=request.POST['email'], first_name=request.POST['name'])
    # Profile.objects.filter(user=empl_id).update(organization=request.POST['org'])
    messages.success(request, 'Updated successfully!')
    return redirect('emplList')


@login_required(login_url='login')
def deleteEmpl(request, empl_id):
    user = get_object_or_404(User, pk=empl_id)
    user.delete()
    messages.success(request, 'Deleted successfully!')
    return redirect('emplList')


@user_passes_test(lambda u: u.is_superuser)
@login_required(login_url='login')
def organization(request):
    if request.method == 'POST':
        organization = Organization()
        organization.name = request.POST['org_name']
        organization.save()
        messages.success(request, 'Saved successfully!')
        return redirect('organization')
    else:
        org_list = Organization.objects.all()
        return render(request, 'survey/organization.html', {"org_list": org_list})


@user_passes_test(lambda u: u.is_superuser)
@login_required(login_url='login')
def updateOrg(request):
    Organization.objects.filter(id=request.POST['org_id']).update(name=request.POST['name'])
    messages.success(request, 'Updated successfully!')
    return redirect('organization')


@user_passes_test(lambda u: u.is_superuser)
@login_required(login_url='login')
def deleteOrg(request, org_id):
    org = get_object_or_404(Organization, pk=org_id)
    org.delete()
    messages.success(request, 'Deleted successfully!')
    return redirect('organization')


@user_passes_test(lambda u: u.is_superuser)
@login_required(login_url='login')
def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        # return redirect('home')
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')


# Questions curds
@login_required(login_url='login')
def questList(request):
    questions_list = Questions_library.objects.filter(created_by=request.user.id)
    return render(request, 'survey/questions.html', {"questions_list": questions_list})


class AddQuest(ListView):
    context_object_name = 'survey_questions_library'
    model = models.Questions_library
    template_name = 'survey/add_questions.html'


@user_passes_test(lambda u: u.is_org_admin)
@login_required(login_url='login')
def saveQuest(request):
    if request.method == 'POST':
        quest = Questions_library()
        quest.title = request.POST['title']
        quest.type = request.POST['type']
        quest.created_by = User.objects.get(id=request.user.id)
        quest.save()
        if request.POST['choices']:

            for x in request.POST['choices'].split(','):
                ques_c = ques_choices()
                ques_c.questions = quest
                ques_c.choice = x
                ques_c.created_by = User.objects.get(id=request.user.id)
                ques_c.save()
        messages.success(request, 'Added successfully!')
        return redirect('questList')


@user_passes_test(lambda u: u.is_org_admin)
@login_required(login_url='login')
def updateQuest(request):
    Questions_library.objects.filter(id=request.POST['quest_id']).update(title=request.POST['title'])
    messages.success(request, 'Updated successfully!')
    return redirect('questList')


@user_passes_test(lambda u: u.is_superuser)
@login_required(login_url='login')
def deleteQuestion(request, quest_id):
    print(id)
    questions_library = get_object_or_404(Questions_library, pk=quest_id)
    questions_library.delete()
    messages.success(request, 'Deleted successfully!')
    return redirect('questList')


# Survey curd
@user_passes_test(lambda u: u.is_org_admin)
@login_required(login_url='login')
def surveyList(request):
    survey_list = Survey.objects.filter(created_by=request.user.id)
    return render(request, 'survey/survey.html', {"survey_list": survey_list})


@user_passes_test(lambda u: u.is_org_admin)
@login_required(login_url='login')
def addSurvey(request):
    questions_list = Questions_library.objects.filter(created_by=request.user.id)
    return render(request, 'survey/add_survey.html', {"questions_list": questions_list})


@user_passes_test(lambda u: u.is_org_admin)
@login_required(login_url='login')
def surveyQuest(request, survey_id):
    survey_questions_list = Survey_QuesMap.objects.filter(survey_id=survey_id)
    survey_employee_list = SurveyEmployeeMap.objects.filter(survey_id=survey_id)
    return render(request, 'survey/survey_questions_list.html', {"survey_questions_list": survey_questions_list,
                                                                 "survey_employee_list": survey_employee_list})


@user_passes_test(lambda u: u.is_org_admin)
@login_required(login_url='login')
def saveSurvey(request):
    if request.method == 'POST':
        surveyObj = Survey()
        surveyObj.name = request.POST['name']
        surveyObj.s_date = request.POST['s_date']
        surveyObj.e_date = request.POST['e_date']
        surveyObj.created_by = User.objects.get(id=request.user.id)
        surveyObj.save()
        if request.POST['question_id']:
            for quest_id in request.POST.getlist('question_id'):
                SurveyQuesMapObj = Survey_QuesMap()
                SurveyQuesMapObj.survey_id = surveyObj
                SurveyQuesMapObj.question_id = get_object_or_404(Questions_library, pk=quest_id)
                SurveyQuesMapObj.created_by = User.objects.get(id=request.user.id)
                SurveyQuesMapObj.save()
        messages.success(request, 'Added successfully!')
        return redirect('surveyList')


@user_passes_test(lambda u: u.is_org_admin)
@login_required(login_url='login')
def deleteSurvey(request, survey_id):
    print(id)
    surveyObj = get_object_or_404(Survey, pk=survey_id)
    surveyObj.delete()
    messages.success(request, 'Deleted successfully!')
    return redirect('surveyList')


@user_passes_test(lambda u: u.is_org_admin)
@login_required(login_url='login')
def assignSurvey(request, survey_id):
    user_list = User.objects.filter(organization= request.user.organization, is_org_admin=False)
    messages.success(request, 'Survey Assign successfully!')
    return render(request, 'survey/survey_assign.html', {"user_list": user_list, "survey_id": survey_id})


@user_passes_test(lambda u: u.is_org_admin)
@login_required
def saveAssignSurvey(request):
    if request.POST['emp_id']:
        for employee_id in request.POST.getlist('emp_id'):
            surveyEmployee = SurveyEmployeeMap.objects.filter(survey_id=request.POST['survey_id'],
                                                           empl_id=employee_id)
            if not surveyEmployee:
                surveyEmployeeMapObj = SurveyEmployeeMap()
                surveyEmployeeMapObj.survey_id = get_object_or_404(Survey, pk=request.POST['survey_id'])
                surveyEmployeeMapObj.empl_id = get_object_or_404(User, pk=employee_id)
                surveyEmployeeMapObj.created_by = User.objects.get(id=request.user.id)
                surveyEmployeeMapObj.save()
                userObj = get_object_or_404(User, pk=employee_id)
                to_email = userObj.email
                try:
                    email_body = "Hi, \nYour Survey Link: "+request.build_absolute_uri('/')[:-1].strip("/")+"/"+request.POST['survey_id']+"/surveyQuestEmployee/"
                    email = EmailMessage(
                        'Survey Assign', email_body, to=[to_email]
                    )
                    email.send()
                except Exception as e:
                    print(e)
    messages.success(request, 'Saved successfully!')
    return redirect('surveyList')


# Employee
@login_required(login_url='login')
def surveyListEmployee(request):
    survey_list_empl = SurveyEmployeeMap.objects.filter(empl_id=request.user.id)
    survey_list_assign_empl = list()
    survey_list_pending_empl = list()
    survey_list_complete_empl = list()
    for survey in survey_list_empl:
        survey_item = Survey_Result.objects.filter(survey=survey.survey_id_id,
                                                   empl=User.objects.get(id=request.user.id)).count()
        if survey_item:
            if Survey_Result.objects.filter(survey=survey.survey_id_id,
                                                   empl=User.objects.get(id=request.user.id),
                                            answer_status=True).count():
                survey_list_complete_empl.append(survey)
            else:
                survey_list_pending_empl.append(survey)
        else:
            survey_list_assign_empl.append(survey)

    return render(request, 'survey/survey_employee.html', {"survey_list_assign_empl": survey_list_assign_empl,
                                                           "survey_list_complete_empl": survey_list_complete_empl,
                                                           "survey_list_pending_empl":survey_list_pending_empl})


@login_required(login_url='login')
def surveyQuestEmployee(request, survey_id):
    question_ids = list()
    survey_questions_list = Survey_QuesMap.objects.filter(survey_id=survey_id)
    for que in survey_questions_list:
        question_ids.append(que.question_id_id)

    choices = ques_choices.objects.filter(questions_id__in=question_ids)

    answer_list = Survey_Result.objects.filter(question_id__in=question_ids, survey_id=survey_id, empl_id=User.objects.get(id=request.user.id))
    paginator = Paginator(survey_questions_list, 3)
    page = request.GET.get('page')
    survey_questions = paginator.get_page(page)

    return render(request, 'survey/survey_questions_list_empl.html', {"survey_id": survey_id,
                                    "survey_questions_list": survey_questions, 'choices': choices,
                                    "answer_list": answer_list})


@login_required(login_url='login')
def saveSurveyAnswers(request, survey_id):
    count = 1
    page = request.GET.get('page')

    for name in request.POST:
        count += 1
        if name != "csrfmiddlewaretoken" and name != "save":
            if request.POST["save"] == "finish":
                isRecord = Survey_Result.objects.filter(survey=Survey.objects.get(id=survey_id),
                                                        empl=User.objects.get(id=request.user.id),
                                                        question=Questions_library.objects.get(id=name))
                if isRecord:
                    Survey_Result.objects.filter(survey=Survey.objects.get(id=survey_id),
                                                 empl=User.objects.get(id=request.user.id)).update(answer_status='True')

                else:
                    if request.POST[name]:
                        person, created = Survey_Result.objects.get_or_create(survey=Survey.objects.get(id=survey_id),
                                                                          empl=User.objects.get(id=request.user.id),
                                                                          question=Questions_library.objects.get(id=name),
                                                                          defaults={"answer": request.POST[name],
                                                                                    "answer_status": True})


                if len(request.POST) == count:
                    try:
                        employee = User.objects.get(id=request.user.id)
                        email_body = "Hi, \nThank you for completing your Survey \n\nYour completed survey Link: " + request.build_absolute_uri(
                            '/')[:-1].strip("/") + "/" + \
                                     survey_id + "/surveyQuestResultEmployee/"
                        email = EmailMessage(
                            'Survey Completed', email_body, to=[employee.email]
                        )
                        email.send()
                    except Exception as e:
                        print(e)
                    messages.success(request, 'Submitted successfully!')
                    return redirect('surveyListEmployee')

            else:
                if request.POST[name]:
                    person, created = Survey_Result.objects.get_or_create(survey=Survey.objects.get(id=survey_id),
                                                              empl=User.objects.get(id=request.user.id),
                                                              question=Questions_library.objects.get(id=name),
                                                              defaults={"answer": request.POST[name], "answer_status": False})

    return redirect(str(survey_id) + '/surveyQuestEmployee/' + '?page=' + page)



@login_required(login_url='login')
def surveyQuestResultEmployee(request, survey_id):
    survey_result_quest = Survey_Result.objects.filter(survey=survey_id, empl=User.objects.get(id=request.user.id))
    paginator = Paginator(survey_result_quest, 4)
    page = request.GET.get('page')
    result_quest = paginator.get_page(page)
    return render(request, "survey/survey_questions_result_empl.html", {"survey_result_quest": result_quest})


