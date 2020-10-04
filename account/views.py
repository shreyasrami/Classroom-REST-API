
# Create your views here.

from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.views import View
from django.shortcuts import redirect
from django.contrib.auth.models import auth
from .serializers import RegisterTeacherSerializer,RegisterStudentSerializer,LoginSerializer
from django.contrib import auth
from rest_framework import generics
from rest_framework.authtoken.models import Token
    
class RegisterTeacher(generics.GenericAPIView):
    serializer_class = RegisterTeacherSerializer
    def post(self,request,*args,**kwargs):
        serializer = RegisterTeacherSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            user = serializer.save()
            token = Token.objects.create(user=user).key
            data = {
                'response' : 'Teacher account successfully created',
                'email' : user.email,
                'subject' : user.subject,
                'token' : token
            }
        else:
            data = serializer.errors
        return Response(data)
    


class RegisterStudent(generics.GenericAPIView):
    serializer_class = RegisterStudentSerializer
    def post(self,request,*args,**kwargs):
        serializer = RegisterStudentSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            user = serializer.save()
            token = Token.objects.create(user=user).key
            data = {
                'response' : 'Student account successfully created',
                'sap_id' : user.sap_id,
                'email' : user.email,
                'token' : token
            }
        else:
            data = serializer.errors
        return Response(data)
        
        
class Login(generics.GenericAPIView):
    serializer_class = LoginSerializer
    def post(self,request,*args,**kwargs):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            user = auth.authenticate(email=email,password=password)
            token = Token.objects.get(user=user).key
            if user is not None:
                auth.login(request,user)
                data = {'response' : 'User successfully logged in', 'token' : token}
            else:                                                                                                    
                data = {'response' : 'Invalid Email or Password', 'token' : token}      
        else:
            data = serializer.errors
        return Response(data)

class Logout(View):
    def get(self,request,*args,**kwargs):
        auth.logout(request)
        return redirect('/')

        
