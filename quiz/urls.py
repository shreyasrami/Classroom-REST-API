from django.urls import path
from . import views



urlpatterns = [
    
    path('',views.DisplayQuizzes.as_view(),name='display_quizzes'),
    path('display-questions/<quiz_id>',views.DisplayQuestions.as_view(),name='display_questions'),
    path('create-info/',views.CreateInfo.as_view(),name='create_info'),
    path('create/<quiz_id>',views.Create.as_view(),name='create'),
    path('delete-quiz/<quiz_id>',views.Delete.as_view(),name='delete_quiz'),
    path('delete-question/<question_id>',views.Delete.as_view(),name='delete_question'),
    path('update-question/<question_id>',views.UpdateQuestion.as_view(),name='update_question'),
    path('update-quiz/<quiz_id>',views.UpdateQuiz.as_view(),name='update_quiz')
    
]    