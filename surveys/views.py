import json
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template.defaulttags import register
from django.urls import reverse
from django.utils import timezone

from accounts.decorators import email_verified, ban_check, limits_check
from surveys.models import Survey, SurveyAnswer, SurveyQuestion, Commentary


@login_required(login_url='user_login')
@ban_check(redirect_html='permissionError.html', parameters_permanent={'code': 3}, parameters_temporary={'code': 2})
@limits_check(redirect_html='permissionError.html', parameters={'code': 1})
@email_verified(messages=['Your email is not verified'])
def createSurvey(request):

    if request.is_ajax():
        # <editor-fold desc="CHECKS">
        checked = False

        title = request.POST.get('title')
        description = request.POST.get('description')

        linkAccess = request.POST.get('linkAccess')
        if linkAccess == 'true':
            linkAccess = True
        else:
            linkAccess = False

        linkAccess_text = request.POST.get('linkAccess-text-survey')

        if not check_string(title):
            messages.error(request, "Incorrect title")
        if not check_string(description):
            messages.error(request, "Incorrect description")
        if not linkAccess_text.isalnum():
            messages.error(request, "Link may only contain digits and letters and should not be empty")

        questionFilled = True
        filled = True
        different = True
        questionDifferent = True
        stop = 0
        enoughAnswers = True

        i = 0
        while request.POST.get(f'question{i + 1}', default=None) != None:
            if not check_string(request.POST.get(f'question{i + 1}')):
                questionFilled = False
            for j in range(i):
                if request.POST.get(f'question{i + 1}') == request.POST.get(f'question{j + 1}'):
                    questionDifferent = False
                    break
            for j in range(10):
                if request.POST.get(f'answer{i + 1}_{j + 1}', default=None) != None:
                    if not check_string(request.POST.get(f'answer{i + 1}_{j + 1}')):
                        filled = False
                    for k in range(j):
                        if request.POST.get(f'answer{i + 1}_{j + 1}') == request.POST.get(f'answer{i + 1}_{k + 1}'):
                            different = False
                            break
                else:
                    stop = j
                    break
            if stop <= 1:
                enoughAnswers = False
            i += 1

        if i == 0:
            messages.error(request, "Number of questions should be at least 1")
        if not questionDifferent:
            messages.error(request, "Questions should be different")
        if not questionFilled:
            messages.error(request, "Questions should not be empty")
        if not enoughAnswers:
            messages.error(request, "Number of answers for each question should be at least 2")
        if not different:
            messages.error(request, "Answers for each question should be different")
        if not filled:
            messages.error(request, "Answers should not be empty")
        if len(messages.get_messages(request)) == 0:
            checked = True
        # </editor-fold>

        data = {}
        data['success'] = True

        if checked:
            linkCheck = True
            try:
                survey = Survey.objects.get(url=linkAccess_text)
            except ObjectDoesNotExist:
                pass
            else:
                linkCheck = False
                messages.error(request, "Survey with such link already exists")


            if linkCheck:
                survey = Survey(title=title, description=description, url=linkAccess_text,
                                isLocked=linkAccess, creator=User.objects.get(username=request.user.username))
                survey.save()

                i = 0
                while request.POST.get(f'question{i + 1}', default=None) != None:
                    surveyQuestion = SurveyQuestion(survey=survey, text=request.POST.get(f'question{i + 1}'), multipleChoice=(request.POST.get(f'multichoice{i + 1}')=='true'))
                    surveyQuestion.save()
                    for j in range(10):
                        if request.POST.get(f'answer{i + 1}_{j + 1}', default=None) != None:
                            surveyAnswer = SurveyAnswer(surveyQuestion=surveyQuestion, text=request.POST.get(f'answer{i + 1}_{j + 1}'))
                            surveyAnswer.save()
                        else:
                            break
                    i += 1

        if len(messages.get_messages(request)) == 0:
            messages.success(request, 'Check succeeded')

        # <editor-fold desc="SEND-MESSAGES">
        sended_messages = []
        for message in messages.get_messages(request):
            sended_messages.append({
                "level": message.level,
                "message": message.message,
                "extra_tags": message.tags,
            })
        data['messages'] = sended_messages
        # </editor-fold>

        return HttpResponse(json.dumps(data), content_type="application/json")
    context = {
        'answers_len': 5,
    }
    return render(request, 'surveyCreation.html', context)

@login_required(login_url='user_login')
@ban_check(redirect_html='permissionError.html', parameters_permanent={'code': 3}, parameters_temporary={'code': 2})
@email_verified(messages=['Your email is not verified'])
def passSurvey(request):
    survey_url = request.GET.get('survey', None)
    try:
        survey = Survey.objects.get(url=survey_url)
    except:
        return redirect(reverse('main'))

    if request.is_ajax():
        change = request.POST.get('rating_change', None)
        if change is not None:
            data = {
                'btn_change': '0',
            }
            if change == '1':
                try:
                    survey.upped.get(username=request.user.username)
                except:
                    survey.upped.add(request.user)
                    data['btn_change'] = '1'
                    survey.rating += 1
                    try:
                        survey.downed.get(username=request.user.username)
                    except:
                        pass
                    else:
                        survey.downed.remove(request.user)
                        survey.rating += 1
                else:
                    survey.upped.remove(request.user)
                    survey.rating -= 1
                survey.save()
            elif change == '-1':
                try:
                    survey.downed.get(username=request.user.username)
                except:
                    survey.downed.add(request.user)
                    data['btn_change'] = '-1'
                    survey.rating -= 1
                    try:
                        survey.upped.get(username=request.user.username)
                    except:
                        pass
                    else:
                        survey.upped.remove(request.user)
                        survey.rating -= 1
                else:
                    survey.downed.remove(request.user)
                    survey.rating += 1
                survey.save()
            data['count_like'] = survey.upped.count()
            data['count_dislike'] = survey.downed.count()
            return HttpResponse(json.dumps(data), content_type="application/json")
        elif (lock_change := request.POST.get('change_lock', None)) is not None:
            survey.isLocked = not survey.isLocked
            survey.save()
            data = {
                'btn_change': '1',
            }
            if survey.isLocked:
                data['btn_change'] = '0'
            return HttpResponse(json.dumps(data), content_type="application/json")


    questions = SurveyQuestion.objects.filter(survey=survey)
    answers = []
    for i in range(len(questions)):
        answers.append(SurveyAnswer.objects.filter(surveyQuestion=questions[i]))

    participated = False
    for answers_group in answers:
        for answer in answers_group:
            try:
                answer.users.get(username=request.user.username)
                participated = True
                break
            except:
                pass
        if participated:
            break

    rootComments = Commentary.objects.filter(survey=survey).order_by('creationTime')
    comments = []
    for comment in rootComments:
        childComments = Commentary.objects.filter(rootComment=comment).order_by('creationTime')
        comments.append([comment, childComments])

    context = {
        'survey': survey,
        'notPassed': not participated,
        'comments': comments,
    }

    if not participated:
        context['answers'] = zip(questions, answers, [i + 1 for i in range(len(questions))])
        if request.method == 'POST':
            for i in range(len(answers)):
                answers_i = request.POST.getlist(f'answers_inp{i + 1}')
                for answer in answers_i:
                    print(answer)
                    answer = SurveyAnswer.objects.get(surveyQuestion=questions[i], text=answer)
                    answer.users.add(request.user)
                    answer.save()
            return redirect(reverse('survey_pass') + f'?survey={survey_url}')
    else:
        answers_stats = []
        users = []
        for i in range(len(answers)):
            answers_stats.append([])
            users.append(set())
            for answer in answers[i]:
                for user in answer.users.all():
                    users[i].add(user)
            for answer in answers[i]:
                answers_stats[i].append([answer.text, answer.users.count(), f'{int(100 * answer.users.count() / len(users[i]))}%'])

        context['answers'] = zip(questions, answers_stats)

    context['rated'] = 0
    try:
        survey.upped.get(username=request.user.username)
    except:
        try:
            survey.downed.get(username=request.user.username)
        except:
            pass
        else:
            context['rated'] = -1
    else:
        context['rated'] = 1

    context['old'] = ((timezone.now() - survey.creationTime).days * 24 + (timezone.now() - survey.creationTime).seconds / 3600) >= 12

    return render(request, 'surveyVoting.html', context)

@login_required(login_url='user_login')
@ban_check(redirect_html='permissionError.html', parameters_permanent={'code': 3}, parameters_temporary={'code': 2})
@limits_check(redirect_html='permissionError.html', parameters={'code': 1})
def editSurvey(request):
    survey = request.GET.get('survey', None)
    try:
        survey = Survey.objects.get(url=survey)
    except:
        return redirect(reverse('main'))
    if survey.creator != None and survey.creator.username != request.user.username:
        return redirect(reverse('main'))

    if request.is_ajax():
        data = {}
        if request.POST.get('delete', default=False) == 'true':
            print('Delete')
            survey.delete()
            response = HttpResponseRedirect(reverse('main'))
            response.status_code = 278
            return response
        else:
            # <editor-fold desc="CHECKS">
            checked = False

            title = request.POST.get('title')
            description = request.POST.get('description')

            linkAccess = request.POST.get('linkAccess')
            if linkAccess == 'true':
                linkAccess = True
            else:
                linkAccess = False

            if not check_string(title):
                messages.error(request, "Incorrect title")
            if not check_string(description):
                messages.error(request, "Incorrect description")

            questionFilled = True
            filled = True
            different = True
            questionDifferent = True
            stop = 0
            enoughAnswers = True

            i = 0
            while request.POST.get(f'question{i + 1}', default=None) != None:
                if not check_string(request.POST.get(f'question{i + 1}')):
                    questionFilled = False
                for j in range(i):
                    if request.POST.get(f'question{i + 1}') == request.POST.get(f'question{j + 1}'):
                        questionDifferent = False
                        break
                for j in range(10):
                    if request.POST.get(f'answer{i + 1}_{j + 1}', default=None) != None:
                        if not check_string(request.POST.get(f'answer{i + 1}_{j + 1}')):
                            filled = False
                        for k in range(j):
                            if request.POST.get(f'answer{i + 1}_{j + 1}') == request.POST.get(f'answer{i + 1}_{k + 1}'):
                                different = False
                                break
                    else:
                        stop = j
                        break
                if stop <= 1:
                    enoughAnswers = False
                i += 1

            if i == 0:
                messages.error(request, "Number of questions should be at least 1")
            if not questionDifferent:
                messages.error(request, "Questions should be different")
            if not questionFilled:
                messages.error(request, "Questions should not be empty")
            if not enoughAnswers:
                messages.error(request, "Number of answers for each question should be at least 2")
            if not different:
                messages.error(request, "Answers for each question should be different")
            if not filled:
                messages.error(request, "Answers should not be empty")
            if len(messages.get_messages(request)) == 0:
                checked = True
            # </editor-fold>

            data['success'] = True

            if checked:
                for question in SurveyQuestion.objects.filter(survey=survey):
                    question.delete()
                survey.rating = 0
                survey.downed.clear()
                survey.upped.clear()
                survey.save()
                i = 0
                while request.POST.get(f'question{i + 1}', default=None) != None:
                    surveyQuestion = SurveyQuestion(survey=survey, text=request.POST.get(f'question{i + 1}'), multipleChoice=(request.POST.get(f'multichoice{i + 1}')=='true'))
                    surveyQuestion.save()
                    for j in range(10):
                        if request.POST.get(f'answer{i + 1}_{j + 1}', default=None) != None:
                            surveyAnswer = SurveyAnswer(surveyQuestion=surveyQuestion, text=request.POST.get(f'answer{i + 1}_{j + 1}'))
                            surveyAnswer.save()
                        else:
                            break
                    i += 1

            if len(messages.get_messages(request)) == 0:
                messages.success(request, 'Check succeeded')

        # <editor-fold desc="SEND-MESSAGES">
        sended_messages = []
        for message in messages.get_messages(request):
            sended_messages.append({
                "level": message.level,
                "message": message.message,
                "extra_tags": message.tags,
            })
        data['messages'] = sended_messages
        # </editor-fold>

        return HttpResponse(json.dumps(data), content_type="application/json")

    questions = SurveyQuestion.objects.filter(survey=survey)
    answers = []
    for i in range(len(questions)):
        objects = SurveyAnswer.objects.filter(surveyQuestion=questions[i])
        answers.append(zip(objects, [j + 1 for j in range(objects.count())]))

    context = {
        'survey': survey,
    }

    context['answers'] = zip(questions, answers, [i + 1 for i in range(len(questions))])


    return render(request, 'surveyEditing.html', context)

# <editor-fold desc="UTILITY">
def check_string(string):
    return not string.isspace() and len(string) > 0

@register.filter
def get_range(value):
    return range(1, value + 1)
#</editor-fold>