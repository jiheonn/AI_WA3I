from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from mainpage.models import *
from .models import User
from django.http import JsonResponse
from django.db.models import Q

import datetime
import string
import random
import json

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect


# def index(request):
#     return HttpResponse("Hello, world. You're at the polls index.")

def index(request):
    context = {

    }
    return render(request, 'teacher/index.html', context)


def question_selection(request):
    category_data = Category.objects.all()
    now = datetime.datetime.now()
    now_date = now.strftime('%Y-%m-%d')
    question_data = Question.objects.all()

    assignment_id = Assignment.objects.all().values('assignment_id')

    context = {
        'question_data': question_data,
        'assignment_id': assignment_id,
        'category_data': category_data
    }
    try:
        select_code_list = request.GET.getlist('question')
        assignment_data = Assignment(assignment_id=request.GET['code_num'],
                                     teacher=Teacher.objects.get(teacher_id=2),
                                     assignment_title=request.GET['question-title'],
                                     type=request.GET['evaluation_type'],
                                     start_date=datetime.datetime.strptime(request.GET['start-date'],
                                                                           '%Y-%m-%d').date(),
                                     end_date=datetime.datetime.strptime(request.GET['end-date'], '%Y-%m-%d').date(),
                                     made_date=now_date,
                                     grade=int(request.GET['grade']),
                                     school_class=int(request.GET['class']))
        assignment_data.save()

        for i in select_code_list:
            asi_qst_rel_data = AssignmentQuestionRel(
                question_id=int(i),
                assignment_id=request.GET['code_num']
            )

            asi_qst_rel_data.save()

        return HttpResponseRedirect(request.GET['path'])

    except:
        assignment_data = None

    return render(request, 'teacher/question_selection.html', context)


def view_result(request):
    assignment_data = Assignment.objects.all().order_by('start_date')
    context = {
        'assignment_data': assignment_data
    }
    return render(request, 'teacher/view_result.html', context)


def make_question(request):
    now = datetime.datetime.now()
    now_date = now.strftime('%Y-%m-%d')
    context = {
    }

    try:
        make_question_data = MakeQuestion(teacher=Teacher.objects.get(teacher_id=2),
                                          question_name=request.POST['question_name'],
                                          discription=request.POST['discription'],
                                          answer=request.POST['answer'],
                                          image=request.FILES['image'],
                                          hint=request.POST['hint'],
                                          made_date=now_date,
                                          upload_check=0)
        make_question_data.save()

        mark_list = request.POST.getlist('mark_text')
        temp = MakeQuestion.objects.get(hint=request.POST['hint'], made_date=now_date)
        for i in mark_list:
            mark_data = Mark(mark_text=i,
                             make_question_id=temp.make_question_id)
            mark_data.save()

        return HttpResponseRedirect(request.POST['path'])

    except:
        make_question_data = None

    return render(request, 'teacher/make_question.html', context)


def bigram_tree(request):
    context = {
    }
    return render(request, 'teacher/bigram_tree.html', context)


def topic_analysis(request):
    context = {
    }
    return render(request, 'teacher/topic_analysis.html', context)


def response_analysis(request):
    context = {
    }
    return render(request, 'teacher/response_analysis.html', context)


def qr_code(request):
    question_data = Question.objects.all()
    context = {
        'question_data': question_data
    }
    return render(request, 'teacher/QR_code.html', context)


def teacher_notice(request):
    context = {
    }
    return render(request, 'teacher/teacher_notice.html', context)


def view_result_detail(request):
    select_code = request.GET['select_code']
    assignment_data = Assignment.objects.all().filter(assignment_id=select_code)
    solve_data = Solve.objects.select_related('as_qurel').filter(
        as_qurel_id__assignment_id=select_code).order_by('student_id')
    question_count = solve_data.values('as_qurel_id__question_id').distinct().count()  # 문항 수

    result = {}
    for i in solve_data:
        # print(i)
        test = {}
        if i.student_id in result:
            result[i.student_id]['student_id'] = i.student_id
            result[i.student_id]['student_score'].append(int(i.score))
            result[i.student_id]['student_response'].append(i.response)
        else:
            test['student_progress'] = []
            test['student_score'] = []
            test['student_response'] = []
            test['student_id'] = i.student_id
            test['student_name'] = i.student_name
            # test['student_response'] = i.solve.response
            test['student_score'].append(int(i.score))
            test['student_response'].append(i.response)

            result[i.student_id] = test

    # print(result)
    for data_row in result:
        check_data = result[data_row]
        result[data_row]['student_score'] = sum(check_data['student_score']) / len(check_data['student_score'])
    # print(result.values())

    try:
        total = 0
        total_pgs = 0
        for j in result.values():
            total += j['student_score']
            if len(j['student_response']) >= 1:
                for c in j['student_response']:
                    count = len(j['student_response'])
                    pgs = count / question_count * 100
            j['student_progress'] = round(pgs)
            total_pgs += j['student_progress']
            # print(j['student_progress'])
        # print(len(result.values()))
        # print(total, len(result.values()))
        all_avg = total / len(result.values())
        all_pgs = round(total_pgs / len(result.values()))
    except ZeroDivisionError:
        all_avg = 0
        all_pgs = 0

    context = {
        'assignment_data': assignment_data,
        'question_count': question_count,
        'result': result.values(),
        'result_item': result.items(),
        'all_avg': round(all_avg, 2),
        'all_pgs': all_pgs

    }
    return render(request, 'teacher/view_result_detail.html', context)


def change_qr_code(request):
    question_name = request.GET['question_name']
    qst_data = Question.objects.all().filter(question_name=question_name)

    question_data = []
    for i in qst_data:
        question_data_dict = dict()
        question_data_dict['QR_code'] = json.dumps(str( i.qr_code)).replace('"', '')
        question_data.append(question_data_dict)

    context = {
        'question_data': question_data
    }
    return JsonResponse(context)


def question_search(request):
    user_input = request.GET['user_input']

    # sah_data = Keyword.objects.select_related('question').filter(keyword_name__icontains=user_input)
    sah_data = Keyword.objects.select_related('question').filter(keyword_name__icontains=user_input).values_list(
        'question_id', flat=True).distinct()
    data = Question.objects.filter(pk__in=sah_data)
    search_data = []
    for i in data:
        search_data_dict = dict()
        search_data_dict['question_id'] = i.question_id
        search_data_dict['question_name'] = i.question_name
        search_data_dict['question_image'] = json.dumps(str(i.image)).replace('"', '')
        search_data.append(search_data_dict)
    # print(search_data)
    context = {
        'search_data': search_data
    }
    return JsonResponse(context)


def view_search(request):
    user_input = request.GET['user_input']
    asi_data = Assignment.objects.all().filter(assignment_title__icontains=user_input)

    assignment_data = []
    for i in asi_data:
        assignment_data_dict = dict()
        assignment_data_dict['assignment_id'] = i.assignment_id
        assignment_data_dict['assignment_title'] = i.assignment_title
        assignment_data_dict['assignment_type'] = i.type
        assignment_data_dict['start_date'] = i.start_date
        assignment_data_dict['end_date'] = i.end_date
        assignment_data_dict['student_grade'] = i.grade
        assignment_data_dict['student_class'] = i.school_class
        assignment_data.append(assignment_data_dict)

    context = {
        'assignment_data': assignment_data
    }
    return JsonResponse(context)


def assignment_copy(request):
    copy_code = request.GET['copy_code']
    # print(copy_code)
    cp_data = AssignmentQuestionRel.objects.select_related('assignment', 'question').filter(assignment_id=copy_code)

    copy_data = []
    for i in cp_data:
        copy_data_dict = dict()
        copy_data_dict['question_id'] = i.question.question_id
        copy_data_dict['assignment_type'] = i.assignment.type
        copy_data_dict['assignment_title'] = i.assignment.assignment_title
        copy_data.append(copy_data_dict)

    context = {
        'copy_data': copy_data
    }
    return JsonResponse(context)


def change_category(request):
    category_option = request.GET['option']
    if category_option == 'select':
        opt_data = Question.objects.all()
    else:
        opt_data = Question.objects.select_related('category').filter(category__category_name=category_option)

    option_data = []
    for i in opt_data:
        option_data_dict = dict()
        option_data_dict['question_id'] = i.question_id
        option_data_dict['question_name'] = i.question_name
        option_data_dict['question_image'] = json.dumps(str(i.image)).replace('"', '')
        option_data.append(option_data_dict)

    context = {
        'option_data': option_data
    }
    return JsonResponse(context)


def code_generation(request):
    generation_code = request.GET['text']
    # print(generation_code)
    assignment_id = Assignment.objects.all().values('assignment_id')
    # print(assignment_id)

    _LENGTH = 8
    string_pool = string.ascii_uppercase + string.digits

    # result = ""
    # for j in range(_LENGTH):
    #     result += random.choice(string_pool)
    # print(result)

    for i in assignment_id:
        if i == generation_code:
            result = ""
            for j in range(_LENGTH):
                result += random.choice(string_pool)
            # print(result)
        else:
            generation_code = generation_code

    context = {
        'generation_code': generation_code
    }
    return JsonResponse(context)


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(username=username, password=password)
        if user is not None:
            print("인증성공")
            login(request, user)
        else:
            print("인증실패")

    return render(request, "teacher/login.html")


def logout_view(request):
    logout(request)
    return redirect("login")


def signup_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        teacher_id = request.POST['teacher_id']

        user = User.objects.create_user(username, email, password)
        user.last_name = last_name
        user.first_name = first_name
        user.teacher_id = teacher_id
        user.save()
        return redirect("login")

    return render(request, "teacher/signup.html")


def chart(request):
    studnet_name = request.POST.getlist('student_name')
    studnet_score = request.POST.getlist('student_score')

    labels = studnet_name
    data = []

    for i in studnet_score:
        data.append(float(i))

    context = {
        'labels': labels,
        'data': data
    }

    return render(request, 'teacher/chart.html', context)
