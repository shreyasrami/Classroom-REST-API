from django.contrib import admin
from .models import Question,Quiz,Answer,Result
# Register your models here.

admin.site.register((Question,Quiz,Answer,Result))