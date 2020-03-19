from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='sysop'),
    path('teacher_data/', views.teacher_data, name='teacher_data'),
    path('quiz_review/', views.quiz_review, name='quiz_review'),
    path('quiz_produce/', views.quiz_produce, name='quiz_produce'),
    path('quiz_download/', views.quiz_download, name='quiz_download'),
    path('notice/', views.notice, name='notice'),
    path('detailed_review/', views.detailed_review, name='detailed_review'),
    path('detailed_quiz/', views.detailed_quiz, name='detailed_quiz')
]