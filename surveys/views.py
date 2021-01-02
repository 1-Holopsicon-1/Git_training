import json
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.defaulttags import register
from django.urls import reverse

from surveys.models import Survey, SurveyAnswer, SurveyQuestion


@login_required(login_url='main')
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

        linkAccess_text = None
        if linkAccess:
            linkAccess_text = request.POST.get('linkAccess-text-survey')

        if not check_string(title):
            messages.error(request, "Incorrect title")
        if not check_string(description):
            messages.error(request, "Incorrect description")
        if linkAccess and not linkAccess_text.isalnum():
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

        if request.POST.get("test"):
            print('Test')
        else:
            print('No Test')

        data = {}
        data['success'] = True

        if checked:
            linkCheck = True
            if linkAccess:
                try:
                    survey = Survey.objects.get(url=linkAccess_text)
                except ObjectDoesNotExist:
                    pass
                else:
                    linkCheck = False
                    messages.error(request, "Survey with such link already exists")

            else:
                found = False
                try:
                    survey = Survey.objects.get(url=title)
                except ObjectDoesNotExist:
                    found = True
                    linkAccess_text = title

                index = 0
                while not found:
                    index += 1
                    try:
                        survey = Survey.objects.get(url=f'{title}_{index}')
                    except ObjectDoesNotExist:
                        found = True
                        linkAccess_text = f'{title}_{index}'


            if linkCheck:
                survey = Survey(title=title, description=description, url=linkAccess_text,
                                isLocked=linkAccess)
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

@login_required(login_url='main')
def passSurvey(request):
    survey = request.GET.get('survey', None)
    try:
        survey = Survey.objects.get(url=survey)
    except:
        return redirect(reverse('main'))

    questions = SurveyQuestion.objects.filter(survey=survey)
    answers = []
    for i in range(len(questions)):
        answers.append(SurveyAnswer.objects.filter(surveyQuestion=questions[i]))
        for answer in SurveyAnswer.objects.filter(surveyQuestion=questions[i]):
            print(answer.text)
            print(answer.users.count())
        print('---')

    participated = False
    for answers_group in answers:
        for answer in answers_group:
            try:
                for user in answer.users.all():
                    print(user.username)
                print(request.user)
                answer.users.get(username=request.user.username)
                participated = True
                break
            except:
                print(answer.text)
                participated = False
        if participated:
            break
    print(participated, request.user)
    context = {
        'survey': survey,
        'notPassed': not participated,
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
            return redirect(reverse('main'))
    else:
        answers_stats = []
        quantity = []
        for i in range(len(answers)):
            answers_stats.append([])
            quantity.append(0)
            for answer in answers[i]:
                quantity[i] += answer.users.count()
            for answer in answers[i]:
                answers_stats[i].append([answer.text, answer.users.count(), f'{int(100 * answer.users.count() / quantity[i])}%'])

        context['answers'] = zip(questions, answers_stats)

    return render(request, 'surveyVoting.html', context)

@login_required(login_url='main')
def editSurvey(request):

    survey = request.GET.get('survey', None)
    try:
        survey = Survey.objects.get(url=survey)
    except:
        return redirect(reverse('main'))

    if survey.creator != request.user:
        return redirect(reverse('main'))

    if request.is_ajax():
        # <editor-fold desc="CHECKS">
        checked = False

        title = request.POST.get('title')
        description = request.POST.get('description')

        multichoice = request.POST.get('multichoice')
        if multichoice == 'true':
            multichoice = True
        else:
            multichoice = False

        if not check_string(title):
            messages.error(request, "Incorrect title")
        if not check_string(description):
            messages.error(request, "Incorrect description")

        filled = True
        different = True
        stop = 0
        for i in range(10):
            if request.POST.get(f'answer{i + 1}', default=None) != None:
                if not check_string(request.POST.get(f'answer{i + 1}')):
                    filled = False
                for j in range(i):
                    if request.POST.get(f'answer{i + 1}') == request.POST.get(f'answer{j + 1}'):
                        different = False
            else:
                stop = i
                break

        if not filled:
            messages.error(request, "Answers should not be empty")
        if stop <= 1:
            messages.error(request, "Number of answers should be at least 2")
        if not different:
            messages.error(request, "Answers should be different")
        if len(messages.get_messages(request)) == 0:
            checked = True
        # </editor-fold>

        data = {}
        data['success'] = True

        if checked:
            answers = SurveyAnswer.objects.filter(survey=survey)
            for i in range(10):
                if request.POST.get(f'answer{i + 1}', default=None) != None:
                    if i < len(answers):
                        answers[i].text = request.POST.get(f'answer{i + 1}')
                        answers[i].users.clear()
                        answers[i].save()
                    else:
                        surveyAnswer = SurveyAnswer(survey=survey, text = request.POST.get(f'answer{i + 1}'))
                        surveyAnswer.save()
                else:
                    for j in range(i, len(answers)):
                        answers[j].delete()
                    break

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
    return render(request, 'surveyEditing.html', context)

# <editor-fold desc="UTILITY">
def check_string(string):
    return not string.isspace() and len(string) > 0

@register.filter
def get_range(value):
    return range(1, value + 1)
#</editor-fold>