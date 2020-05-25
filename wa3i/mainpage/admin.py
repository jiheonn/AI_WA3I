# admin.py
from django.contrib import admin
from .models import *
from rangefilter.filter import DateRangeFilter, DateTimeRangeFilter


class MarkAdmin(admin.ModelAdmin):
    list_display = ['mark_id', 'make_question', 'mark_text']

admin.site.register(Mark, MarkAdmin)

class SelfSolveDataAdmin(admin.ModelAdmin):
    list_display = ['self_id', 'make_question', 'response', 'score', 'submit_date']

admin.site.register(SelfSolveData, SelfSolveDataAdmin)

class MakeQuestionAdmin(admin.ModelAdmin):
    list_display = ['make_question_id', 'teacher', 'question_name', 'discription',
                    'answer', 'image', 'hint', 'made_date', 'check']

admin.site.register(MakeQuestion, MakeQuestionAdmin)

class TeacherAdmin(admin.ModelAdmin):
    list_display = ['teacher_id', 'teacher_name', 'school', 'email',
                    'password', 'approve']

admin.site.register(Teacher, TeacherAdmin)

class AssignmentAdmin(admin.ModelAdmin):
    list_display = ['assignment_id', 'teacher', 'assignment_title', 'type',
                    'start_date', 'end_date', 'made_date', 'grade', 'class_field']
    list_filter = ('type',
                   ('made_date', DateRangeFilter))
    search_fields = ['assignment_title', 'teacher']
admin.site.register(Assignment, AssignmentAdmin)

class StudySolveDataAdmin(admin.ModelAdmin):
    list_display = ['study_id', 'question', 'school', 'gender',
                    'response', 'score', 'submit_date']

admin.site.register(StudySolveData, StudySolveDataAdmin)

admin.site.register(Category)

# class Category_test(models.Model):
#     list_display = ['category_id', 'category_name']
#
# admin.site.register(Category, Category_test)
#

class QuestionAdmin(admin.ModelAdmin):
    list_display = ['question_id','category', 'model_id', 'question_name',
                    'discription','answer','image','hint','made_date',
                    'qr_code','ques_concept']

admin.site.register(Question, QuestionAdmin)

admin.site.register(Keyword)
# class KeywordAdmin(models.Model):
#     list_display = ['keyword_id', 'question_id','keyword_name']
#
# admin.site.register(Keyword, KeywordAdmin)


class SolveAdmin(admin.ModelAdmin):
    list_display = ['solve_id', 'as_qurel', 'student_id', 'submit_date',
                    'response','score', 'student_name']

admin.site.register(Solve, SolveAdmin)

admin.site.register(AssignmentQuestionRel)
# class AssignmentQuestionRelAdmin(models.Model):
#     list_display = ['as_qurel_id', 'assignment', 'question']
#
# admin.site.register(AssignmentQuestionRel, AssignmentQuestionRelAdmin)

class CategoryInlineAdmin(admin.TabularInline):
    model = Category

class AAdmin(admin.ModelAdmin):
     fields = ['question_id', 'keyword_id']
     list_display = ['question_id']
     ordering = ['question_id']
     inlines = [CategoryInlineAdmin]

# admin.site.register(Category)
# admin.site.register(Question)
# admin.site.register(MakeQuestion)
# admin.site.register(Keyword)
# admin.site.register(AssignmentQuestionRel)
# admin.site.register(Mark)
# admin.site.register(Teacher)
# admin.site.register(SelfSolveData)
# admin.site.register(Solve)
# admin.site.register(StudySolveData)
