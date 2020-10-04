
from django.contrib import admin
from account.models import User,Teacher,Student
from rest_framework.authtoken.models import Token

# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("name","username","email")
    list_filter = ("is_admin","is_teacher")
    search_fields = ("first_name","last_name")
    ordering = ("first_name",)

    def save_model(self,request,obj,form,change):
        if form.is_valid():
            password = form.cleaned_data["password"]
            obj.set_password(password)
        obj.save()
        Token.objects.create(user=obj)


    
    
@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ("name","username","email")
    list_filter = ("department","subject",)
    search_fields = ("first_name","last_name")
    ordering = ("first_name",)

    def save_model(self,request,obj,form,change):
        if form.is_valid():
            password = form.cleaned_data["password"]
            obj.set_password(password)
        obj.save()
        Token.objects.create(user=obj)

    

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    
    list_display = ("sap_id","name","email")
    list_filter = ("department","division")
    search_fields = ("sap_id",)
    ordering = ("sap_id",)

    def save_model(self,request,obj,form,change):
        if form.is_valid():
            password = form.cleaned_data["password"]
            obj.set_password(password)
        obj.save()
        Token.objects.create(user=obj)

