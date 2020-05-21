# admin.py
# from django.contrib import admin
# from .models import *
# from rangefilter.filter import DateRangeFilter, DateTimeRangeFilter
# #
# class AssignmentAdmin(admin.ModelAdmin):
#     list_display = ['assignment_id', 'teacher', 'assignment_title', 'type',
#                     'start_date', 'end_date', 'made_date', 'grade', 'class_field']
#     list_filter = ('type',
#                    ('made_date', DateRangeFilter))
#     search_fields = ['assignment_title', 'teacher']
# admin.site.register(Assignment, AssignmentAdmin)

# class AssignmentQuestionRelAdmin(models.Model):
#     list_display = ['as_qurel_id', 'assignment', 'question']
#
# admin.site.register(AssignmentQuestionRel, AssignmentQuestionRelAdmin)

# class CategoryAdmin(models.Model):
#     list_display = ['category_id', 'category_name']
#
# admin.site.register(Category, CategoryAdmin)


# class KeywordAdmin(models.Model):
#     list_display = ['keyword_id', 'question','keyword_name']
#
# admin.site.register(Keyword, KeywordAdmin)
#
# class MakeQuestionAdmin(admin.ModelAdmin):
#     list_display = ['make_question_id', 'teacher', 'question_name', 'discription',
#                     'answer', 'image', 'hint', 'made_date', 'check']
#
# admin.site.register(MakeQuestion, MakeQuestionAdmin)
#
# class Mark(models.Model):
#     mark_id = models.IntegerField(primary_key=True)
#     make_question = models.ForeignKey(MakeQuestion, models.DO_NOTHING, blank=True, null=True)
#     mark_text = models.TextField(blank=True, null=True)
#
# class MarkAdmin(admin.ModelAdmin):
#     list_display = ['mark_id', 'make_question', 'mark_text']
#
# admin.site.register(Mark, MarkAdmin)
#
# class QuestionAdmin(admin.ModelAdmin):
#     list_display = ['assignment_id','category', 'model_id', 'question_name',
#                     'discription','answer','image','hint','made_date',
#                     'qr_code','ques_concept']
#
# admin.site.register(Question, QuestionAdmin)
#
# class SelfSolveDataAdmin(admin.ModelAdmin):
#     list_display = ['self_id', 'make_question', 'response', 'score', 'submit_date']
#
# admin.site.register(SelfSolveData, SelfSolveDataAdmin)
#
# class SolveAdmin(admin.ModelAdmin):
#     list_display = ['solve_id', 'as_qurel', 'student_id', 'submit_date',
#                     'response','score', 'student_name']
#
# admin.site.register(Solve, SolveAdmin)
#
# class StudySolveDataAdmin(admin.ModelAdmin):
#     list_display = ['study_id', 'question', 'school', 'gender',
#                     'response', 'score', 'submit_date']
#
# admin.site.register(StudySolveData, StudySolveDataAdmin)
#
#
# class TeacherAdmin(admin.ModelAdmin):
#     list_display = ['teacher_id', 'teacher_name', 'school', 'email',
#                     'password', 'approve']
#
# admin.site.register(Teacher, TeacherAdmin)

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
