from django.urls import path
from .views import RegisterTeacher,RegisterStudent,Login,Logout
urlpatterns = [
    path('login/',Login.as_view(),name='login'),
    path('register-teacher/',RegisterTeacher.as_view(),name='register_teacher'),
    path('register-student/',RegisterStudent.as_view(),name='register_student'),
    path('logout/',Logout.as_view(),name='logout')
]

