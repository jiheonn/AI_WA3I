from builtins import dict

from django.shortcuts import render, redirect

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
import q as q
from django.db.models import Q
import datetime

from mainpage.models import Question, SelfSolveData, AssignmentQuestionRel, Keyword, Solve, Assignment, MakeQuestion, \
    Category, StudySolveData


def index(request):
    context = {
    }
    return render(request, 'student/index.html', context)


def AI(request):
    qs = Question.objects.all()
    category = Category.objects.all()

    context = {
        'qs': qs,
        'category': category
    }
    return render(request, 'student/AI.html', context)


def AIques(request):
    question_id = int(request.GET['question_id'])
    data = Question.objects.filter(question_id=question_id)[0]
    context = {
        'data': data
    }
    return render(request, 'student/AIques.html', context)


def AIdiag(request):
    question_id = request.GET['question_id']
    ques_ans = request.GET['ques_ans']

    now = datetime.datetime.now()
    now_date = now.strftime('%Y-%m-%d')

    try:
        school = "/static/student/school_gender_img/" + request.GET['category_school'] + ".png"
        gender = "/static/student/school_gender_img/" + request.GET['category_gender'] + ".png"
    except:
        school = ""
        gender = ""

    key = AssignmentQuestionRel.objects.select_related('question').filter(question__question_id=question_id)
    data = key[0]

    # solve테이블과 question테이블 조인
    as_qurel_id = key.values('as_qurel_id')[0]['as_qurel_id']
    da = Solve.objects.prefetch_related('assignment_question_rel').filter(as_qurel_id=as_qurel_id)
    # print(da.query)

    context = {
        'data': data,
        'ques_ans': ques_ans,
        'school': school,
        'gender': gender,
    }
    # return render(request, 'student/AIdiag.html', context)

    # 나의 답 DB에 저장
    # ssd = StudySolveData.objects.select_related('question').filter(question__question_id=question_id)
    try:
        study_solve_data = StudySolveData(
                           question_id=question_id,
                           school=request.GET['category_school'],
                           gender=request.GET['category_gender'],
                           response=ques_ans,
                           score=0,
                           submit_date=now_date
                                          )
        print(study_solve_data)
        study_solve_data.save()

        # return HttpResponseRedirect(request.GET['path'])

    except:
        study_solve_data = None

    return render(request, 'student/AIdiag.html', context)


# def Studyques(request):
#     try:
#         assignment_id = request.GET['code_num']
#         data = AssignmentQuestionRel.objects.select_related('question').filter(assignment_id=assignment_id)
#         # f = data.first()
#
#         da = Assignment.objects.filter(assignment_id=assignment_id)
#
#         if da.values('type')[0]['type'] == "학습평가":
#             f = data.first()
#         else:
#             f = None
#
#     except:
#         question_info = request.GET['question_name'].split(',')
#         question_name = question_info[0]
#         assignment_id = question_info[1]
#
#         data = AssignmentQuestionRel.objects.select_related('question').filter(assignment_id=assignment_id)
#         f = AssignmentQuestionRel.objects.select_related('question').filter(question__question_name=question_name)[0]
#
#     context = {
#         'data': data,
#         'f': f
#     }
#     return render(request, 'student/Studyques.html', context)


def Study(request):
    context = {

    }
    return render(request, 'student/Study.html', context)


def Studyques(request):
    try:
        assignment_id = request.GET['code_num']
        data = AssignmentQuestionRel.objects.select_related('question').filter(assignment_id=assignment_id)
        f = data.first()

    except:
        # 원래 코드
        # question_info = request.GET['question_name'].split(',')
        # question_name = question_info[0]
        # assignment_id = question_info[1]
        #
        # data = AssignmentQuestionRel.objects.select_related('question').filter(assignment_id=assignment_id)
        # f = AssignmentQuestionRel.objects.select_related('question').filter(question__question_name=question_name)[0]

        # 바꾼 코드
        question_info = request.GET['question_id']
        question_id = int(question_info[0])
        assignment_id = question_info[1]

        data = AssignmentQuestionRel.objects.select_related('question').filter(assignment_id=assignment_id)
        f = AssignmentQuestionRel.objects.select_related('question').filter(question__question_id=question_id)[0]

    context = {
        'data': data,
        'f': f
    }
    return render(request, 'student/Studyques.html', context)


def check_code_st(request):
    code_num = request.GET['code_num']

    try:
        code = Assignment.objects.get(assignment_id=code_num)

    except:
        code = None

    if code is None:
        overlap = "fail"
        print("f")
    else:
        overlap = "pass"
        print("p")

        # da = Assignment.objects.filter(assignment_id=assignment_id)
        # if da.values('type')[0]['type'] == "학습평가":

        # types = Assignment.objects.filter(assignment_id=code).values('type')
        #
        # if types == "학습평가":
        #     overlap = "pass"
        # else:
        #     overlap = "fail"

    context = {
        'overlap': overlap
    }
    return JsonResponse(context)


# 테스트
# def check_code_st(request):
#     code_num = request.GET['code_num']
#
#     try:
#         code = Assignment.objects.get(assignment_id=code_num)
#
#     except:
#         code = None
#
#     if code is None:
#         return render(request, 'student/Study.html')
#     else:
#
#         # da = Assignment.objects.filter(assignment_id=assignment_id)
#         # if da.values('type')[0]['type'] == "학습평가":
#
#         types = Assignment.objects.filter(assignment_id=code).values('type')
#
#         if types == "학습평가":
#             return render(request, 'student/Studyques.html')
#         else:
#             return render(request, 'student/Study.html')


def Homework(request):
    context = {
    }
    return render(request, 'student/Homework.html', context)


def Self(request):
    qs = MakeQuestion.objects.all()
    category = Category.objects.all()
    context = {
        'qs': qs,
        'category': category
    }
    return render(request, 'student/Self.html', context)


def Selfques(request):
    make_question_id = int(request.GET['make_question_id'])
    data = MakeQuestion.objects.filter(make_question_id=make_question_id)[0]

    context = {
        'data': data
    }
    return render(request, 'student/Selfques.html', context)


def Selfdiag(request):
    question_id = request.GET['question']
    ques_ans = request.GET['ques_ans']

    # img = MakeQuestion.objects.filter(make_question_id=question_id).get('image')
    # print(img.values())

    data = SelfSolveData.objects.select_related('make_question').filter(make_question_id=question_id)[0]
    # print(data.values())
    context = {
        'data': data,
        'ques_ans': ques_ans,
        # 'img' : img
    }
    return render(request, 'student/Selfdiag.html', context)


def Selfgrade(request):
    context = {
    }
    return render(request, 'student/Selfgrade.html', context)


def Homeworkques(request):
    data = Question.objects.first()
    context = {
        'data': data
    }
    return render(request, 'student/Homeworkques.html', context)


def Homeworkdiag(request):
    # data = AssignmentQuestionRel.objects.select_related('question', 'solve').first()

    re = Solve.objects.prefetch_related('assignment_question_rel').first()
    as_qurel_id = re.values('as_qurel_id')[0]['as_qurel_id']
    data = AssignmentQuestionRel.objects.select_related('question').filter(as_qurel_id=as_qurel_id)

    context = {
        'data': data
    }
    return render(request, 'student/Homeworkdiag.html', context)


def Homeworkselect(request):
    context = {
    }
    return render(request, 'student/Homeworkselect.html', context)


def Homeworklist(request):
    # question_info = request.GET['question_name'].split(',')
    # question_name = question_info[0]
    # assignment_id = question_info[1]
    # data = AssignmentQuestionRel.objects.select_related('question').filter(assignment_id=assignment_id)
    # f = AssignmentQuestionRel.objects.select_related('question').filter(question__question_name=question_name)[0]
    student_id = int(request.GET['ID_num'])
    # rel = AssignmentQuestionRel.objects.select_related('assignment', 'solve').filter(solve__student_id=student_id)

    # 테스트
    re = Solve.objects.prefetch_related('assignment_question_rel').filter(student_id=student_id)
    d = re.values('as_qurel_id')[0]['as_qurel_id']
    print(d)
    rel = AssignmentQuestionRel.objects.prefetch_related('assignment').filter(as_qurel_id=d)

    context = {
        'rel': rel,
        # 'da':da,
        're': re
    }
    return render(request, 'student/Homeworklist.html', context)


def Homeworkcheck(request):
    student_id = int(request.GET['student_id'])
    # assignment_title = request.GET['assignment_id']
    # print(assignment_title.values())
    # data = AssignmentQuestionRel.objects.select_related('assignment', 'question', 'solve').filter(solve__student_id=student_id)

    # 테스트
    re = Solve.objects.prefetch_related('assignment_question_rel').filter(student_id=student_id)
    d = re.values('as_qurel_id')[0]['as_qurel_id']
    print(d)
    data = AssignmentQuestionRel.objects.prefetch_related('assignment', 'question').filter(as_qurel_id=d)

    context = {
        'data': data
    }
    return render(request, 'student/Homeworkcheck.html', context)


def Homeworkcode(request):
    context = {
    }
    return render(request, 'student/Homeworkcode.html', context)


def Notice(request):
    context = {
    }
    return render(request, 'student/Notice.html', context)


def search(request):
    user_input = request.GET['user_input']
    key_data = Keyword.objects.select_related('question').filter(keyword_name__icontains=user_input).values_list(
        'question_id', flat=True).distinct()
    k_data = Question.objects.filter(pk__in=key_data)

    search_data = []
    for i in k_data:
        search_data_dict = dict()
        search_data_dict['question_id'] = i.question_id
        search_data_dict['question_name'] = i.question_name
        search_data_dict['question_image'] = i.image
        search_data.append(search_data_dict)
    context = {
        'search_data': search_data
    }
    return JsonResponse(context)


def search_name(request):
    name_input = request.GET['name_input']
    name_data = MakeQuestion.objects.filter(question_name__icontains=name_input).values_list('make_question_id',
                                                                                             flat=True).distinct()
    n_data = MakeQuestion.objects.filter(pk__in=name_data)

    search_data = []
    for j in n_data:
        search_data_dict = dict()
        search_data_dict['make_question_id'] = j.make_question_id
        search_data_dict['question_name'] = j.question_name
        search_data_dict['question_image'] = j.image
        search_data.append(search_data_dict)
    context = {
        'search_data': search_data
    }
    return JsonResponse(context)


def change_category_self(request):
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
        option_data_dict['question_image'] = i.image
        option_data.append(option_data_dict)

    context = {
        'option_data': option_data
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
        option_data_dict['question_image'] = i.image
        option_data.append(option_data_dict)

    context = {
        'option_data': option_data
    }
    return JsonResponse(context)


def check_code(request):
    code_num = request.GET['code_num']
    # ID_num = int(request.GET['ID_num'])
    try:
        code = Assignment.objects.get(assignment_id=code_num)
    except:
        code = None
    # try:
    #     ID = Solve.objects.filter(student_id=ID_num)
    # except:
    #     ID=None or (ID is None)

    if (code is None):
        overlap = "fail"
    else:
        overlap = "pass"

    context = {
        'overlap': overlap
    }
    return JsonResponse(context)


def check_ID(request):
    ID_num = int(request.GET['ID_num'])

    try:
        ID = Solve.objects.filter(student_id=ID_num)
    except:
        ID = None

    if ID is None:
        overlap = "fail"
    else:
        overlap = "pass"

    context = {
        'overlap': overlap
    }
    return JsonResponse(context)
