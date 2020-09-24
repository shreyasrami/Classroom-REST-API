from .models import User,Teacher,Student
from rest_framework import serializers


class RegisterTeacherSerializer(serializers.ModelSerializer):
    confirm_pass = serializers.CharField(style={'input_type' : 'password'},write_only=True)
    class Meta:
        model = Teacher
        fields = ['first_name', 'last_name', 'username', 'department', 'is_teacher', 'subject', 'email', 'password','confirm_pass']

    def save(self):
        user = Teacher(
            first_name=self.validated_data['first_name'],
            last_name=self.validated_data['last_name'],
            username=self.validated_data['username'],
            department=self.validated_data['department'],
            is_teacher=self.validated_data['is_teacher'],
            subject=self.validated_data['subject'],
            email=self.validated_data['email']

        )
        password = self.validated_data['password']
        confirm_pass = self.validated_data['confirm_pass']
        if password != confirm_pass:
            raise serializers.ValidationError({'password' : 'Passwords does not match'})
        user.set_password(password)
        user.save()
        return user


class RegisterStudentSerializer(serializers.ModelSerializer):
    confirm_pass = serializers.CharField(style={'input_type' : 'password'},write_only=True)
    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'username', 'department', 'is_student', 'division', 'sap_id', 'email', 'password','confirm_pass']
    
    def save(self):
        user = Student(
            first_name=self.validated_data['first_name'],
            last_name=self.validated_data['last_name'],
            username=self.validated_data['username'],
            department=self.validated_data['department'],
            is_student=self.validated_data['is_student'],
            division=self.validated_data['division'],
            sap_id=self.validated_data['sap_id'],
            email=self.validated_data['email']

        )
        password = self.validated_data['password']
        confirm_pass = self.validated_data['confirm_pass']
        if password != confirm_pass:
            raise serializers.ValidationError({'password' : 'Passwords does not match'})
        user.set_password(password)
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=50)
    password = serializers.CharField(style={"input_type": "password"},write_only=True)