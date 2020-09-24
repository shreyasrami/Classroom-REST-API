
# Create your views here.

from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import RegisterTeacherSerializer,RegisterStudentSerializer,LoginSerializer
from django.contrib import auth
from rest_framework import generics

    
class RegisterTeacher(generics.GenericAPIView):
    def post(self,request,*args,**kwargs):
        serializer = RegisterTeacherSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            user = serializer.save()
            data = {
                'response' : 'Teacher account successfully created',
                'email' : user.email,
                'subject' : user.subject,
            }
        else:
            data = serializer.errors
        return Response(data)
    


class RegisterStudent(generics.GenericAPIView):
    def post(self,request,*args,**kwargs):
        serializer = RegisterStudentSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            user = serializer.save()
            data = {
                'response' : 'Student account successfully created',
                'sap_id' : user.sap_id,
                'email' : user.email
            }
        else:
            data = serializer.errors
        return Response(data)
        
        
class Login(generics.GenericAPIView):
    def post(self,request,*args,**kwargs):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            user = auth.authenticate(email=email,password=password)
            if user is not None:
                auth.login(request,user)
                data = {'response' : 'User successfully logged in'}
            else:
                data = {'response' : 'Invalid Email or Password'}      
        else:
            data = serializer.errors
        return Response(data)

        
