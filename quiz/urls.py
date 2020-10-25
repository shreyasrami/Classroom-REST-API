from django.urls import path,include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('',views.QuizViewSet,basename='QuizViewSet')


urlpatterns = [
    
    path('',include(router.urls)),
    path('create/<quiz_id>',views.Create.as_view(),name='create'),
    path('delete-question/<question_id>',views.Delete.as_view(),name='delete_question'),
    path('update-question/<question_id>',views.UpdateQuestion.as_view(),name='update_question'),
    path('attempt-quiz/<quiz_id>',views.AttemptQuiz.as_view(),name='attempt_quiz'),
    path('result/<quiz_id>',views.StudentResult.as_view(),name='result')
    
]    