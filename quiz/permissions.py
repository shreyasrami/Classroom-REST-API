from rest_framework import permissions
from .models import Result,Quiz
from account.models import Student

class IsTeacher(permissions.BasePermission):
    
    def has_permission(self,request,view):
        if request.user.is_teacher:
            return True
        else:
            return False

class IsStudent(permissions.BasePermission):
    
    def has_permission(self,request,view):
        if request.user.is_student:
            return True
        else:
            return False

class NotAttempted(permissions.BasePermission):
    message = "You have already attempted this quiz"
    def has_permission(self,request,view):
        quiz = Quiz.objects.get(id=view.kwargs['quiz_id'])
        student = Student.objects.get(email=request.user)
        if Result.objects.filter(quiz=quiz,student=student).exists():
            return False
        else:
            return True

class HasAttempted(permissions.BasePermission):
    message = "You have not attempted this quiz yet"
    def has_permission(self,request,view):
        if request.user.is_student:
            quiz = Quiz.objects.get(id=view.kwargs['quiz_id'])
            student = Student.objects.get(email=request.user)
            if Result.objects.filter(quiz=quiz,student=student).exists():
                return True
            else:
                return False
        elif request.user.is_teacher:
            return True