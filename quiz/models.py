from django.db import models
from account.models import Teacher
# Create your models here.

class Quiz(models.Model):
    teacher = models.ForeignKey(Teacher,on_delete=models.CASCADE)
    topic = models.CharField(max_length=30)
    total_marks = models.IntegerField()

    def __str__(self):
        return self.topic + '_' + str(self.id)
    
    class Meta:
        verbose_name_plural = 'Quizzes'
    

class Question(models.Model):

    quiz = models.ForeignKey('Quiz',on_delete=models.CASCADE)
    question_text = models.TextField()
    choice1 = models.CharField(max_length=30)
    choice2 = models.CharField(max_length=30)
    choice3 = models.CharField(max_length=30)
    choice4 = models.CharField(max_length=30)
    correct_choice = models.CharField(max_length=30)

    def __str__(self):
        return self.quiz.topic + '_' + str(self.id)

    