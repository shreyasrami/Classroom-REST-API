from rest_framework import permissions

class IsTeacher(permissions.BasePermission):
    
    def has_permission(self,request,view):
        if request.user.is_teacher:
            return True
        else:
            return False
