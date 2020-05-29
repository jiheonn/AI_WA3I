from builtins import dict

from django.shortcuts import render, redirect

# Create your views here.
from django.http import HttpResponse
import q as q
from django.db.models import Q
from django.http import JsonResponse

from mainpage.models import Question, SelfSolveData, AssignmentQuestionRel, Keyword, Solve, Assignment, MakeQuestion

from django.contrib.auth.hashers import check_password
from django.urls import reverse


def index(request):
    context = {
    }
    return render(request, 'student/index.html', context)


def AI(request):
    qs = Question.objects.all()
    context = {
        'qs': qs
    }
    return render(request, 'student/AI.html', context)


#
# def Study(request):
#     if request.method=="GET":
#         return render(request, 'student/Study.html')
#     elif request.method=="POST":
#         code_num = request.POST.get('code_num')
#         ID_num = request.POST.get('ID_num')
#
#         res_data=[]
#         if not (code_num and ID_num):
#             res_data['error']="코드와 아이디 모두 입력하세요."
#         else:
#             fuser = AssignmentQuestionRel.objects.get(assignment_id=code_num)
#
#             if check_password(code_num,fuser.assignment_id):
#                 request.session['user'] = fuser.assignment_id
#                 return redirect(reverse('Study'))
#             else:
#                 res_data['error']="존재하지 않는 코드입니다."
#         return render(request, 'student/Study.html',res_data)

def Study(request):
    context = {

    }
    return render(request, 'student/Study.html', context)


def Homework(request):
    context = {
    }
    return render(request, 'student/Homework.html', context)


def Self(request):
    qs = MakeQuestion.objects.all()
    context = {
        'qs': qs
    }
    return render(request, 'student/Self.html', context)


def AIques(request):
    question_id = int(request.GET['question_id'])
    data = Question.objects.filter(question_id=question_id)[0]

    context = {
        'data': data
    }
    return render(request, 'student/AIques.html', context)


def Studyques(request):
    try:
        # assignment_id = request.GET['code_num']
        # data = AssignmentQuestionRel.objects.select_related('question').filter(assignment_id=assignment_id)
        # f = data.first()

        assignment_id = request.GET['code_num']
        data = AssignmentQuestionRel.objects.select_related('question').filter(assignment_id=assignment_id)
        f = data.first()

        da = Assignment.objects.filter(assignment_id=assignment_id)

        if da.values('type')[0]['type'] == "학습평가":
            f = data.first()
        # else:
        #     print("")
            # print(data.query)

    except:
        question_info = request.GET['question_name'].split(',')
        question_name = question_info[0]
        assignment_id = question_info[1]

        data = AssignmentQuestionRel.objects.select_related('question').filter(assignment_id=assignment_id)
        f = AssignmentQuestionRel.objects.select_related('question').filter(question__question_name=question_name)[0]

    context = {
        'data': data,
        'f': f
    }
    return render(request, 'student/Studyques.html', context)


def Studyques2(request):
    context = {
    }
    return render(request, 'student/Studyques2.html', context)


def Homeworkques(request):
    data = Question.objects.first()
    context = {
        'data': data
    }
    return render(request, 'student/Homeworkques.html', context)


def Selfques(request):
    question_name = request.GET['question']
    data = MakeQuestion.objects.filter(question_name=question_name)[0]

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


def Homeworkdiag(request):
    data = AssignmentQuestionRel.objects.select_related('question', 'solve').first()
    context = {
        'data': data
    }
    return render(request, 'student/Homeworkdiag.html', context)


def AIdiag(request):
    question_id = request.GET['question']
    ques_ans = request.GET['ques_ans']
    try:
        school = "/static/student/school_gender_img/" + request.GET['category_school'] + ".png"
        gender = "/static/student/school_gender_img/" + request.GET['category_gender'] + ".png"
    except:
        school = ""
        gender = ""
    # data = AssignmentQuestionRel.objects.select_related('question','solve').filter(question__question_id=question_id)[0]
    key = AssignmentQuestionRel.objects.select_related('question').filter(question__question_id=question_id)
    data = key[0]

    # solve테이블과 question테이블 조인
    d = key.values('as_qurel_id')[0]['as_qurel_id']
    da = Solve.objects.prefetch_related('assignment_question_rel').filter(as_qurel_id=d)
    print(da.query)

    context = {
        'data': data,
        'ques_ans': ques_ans,
        'school': school,
        'gender': gender,
    }
    return render(request, 'student/AIdiag.html', context)


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
    rel = AssignmentQuestionRel.objects.select_related('assignment', 'solve').filter(solve__student_id=student_id)

    context = {
        'rel': rel
    }
    return render(request, 'student/Homeworklist.html', context)


def Homeworkcheck(request):
    student_id = int(request.GET['student_id'])
    # assignment_title = request.GET['assignment_id']
    # print(assignment_title.values())
    data = AssignmentQuestionRel.objects.select_related('assignment', 'question', 'solve').filter(
        solve__student_id=student_id)

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
    key_data = Keyword.objects.select_related('question').filter(keyword_name__icontains=user_input)

    search_data = []
    for i in key_data:
        search_data_dict = dict()
        search_data_dict['question_id'] = i.question.question_id
        search_data_dict['question_name'] = i.question.question_name
        search_data_dict['question_image'] = i.question.image
        search_data.append(search_data_dict)
    context = {
        'search_data': search_data
    }
    return JsonResponse(context)


def search_name(request):
    name_input = request.GET['name_input']
    name_data = Question.objects.filter(question_name__icontains=name_input)

    search_data = []
    for j in name_data:
        search_data_dict = dict()
        search_data_dict['question_id'] = j.question_id
        search_data_dict['question_name'] = j.question_name
        search_data_dict['question_image'] = j.image
        search_data.append(search_data_dict)
    context = {
        'search_data': search_data
    }
    return JsonResponse(context)


def change_category(request):
    category_option = request.GET['option']
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


def check_code_st(request):
    code_num = request.GET['code_num']
    # ID_num = int(request.GET['ID_num'])
    try:
        code = Assignment.objects.get(assignment_id=code_num)

    except:
        code = None

    if code is None:
        overlap = "fail"
    else:
        overlap = "pass"

        # da = Assignment.objects.filter(assignment_id=assignment_id)
        # if da.values('type')[0]['type'] == "학습평가":

        types = Assignment.objects.filter(assignment_id=code).values('type')[0]['type']
        print(types)
        print("hi")
        # if types == "학습평가":
        #     overlap = "pass"
        # else:
        #     overlap = "fail"

    context = {
        'overlap': overlap
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
