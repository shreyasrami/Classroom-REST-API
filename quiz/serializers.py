from .models import Question,Quiz,Answer
from rest_framework import serializers
from account.models import Teacher


class QuestionSerializer(serializers.ModelSerializer):
    OPTIONS = (
        ('1','Option 1'),
        ('2','Option 2'),
        ('3','Option 3'),
        ('4','Option 4'),

    )
    correct_choice = serializers.ChoiceField(choices=OPTIONS,required=True)
    class Meta:
        model = Question
        fields = ['question_text','choice1','choice2','choice3','choice4','correct_choice']
        labels = {
            "quiz" : "Quiz",
            "question_text" : "Question",
            "choice1" : "Option 1",
            "choice2" : "Option 2",
            "choice3" : "Option 3",
            "choice4" : "Option 4",
            "correct_choice" : "Correct Option"
        }
        


class QuizSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)
    class Meta:
        model = Quiz
        fields = ['id','topic','total_marks','questions']
    
    def create(self,validated_data):
        teacher = Teacher.objects.get(email=self.context.get('request').user)
        validated_data['teacher'] = teacher
        return Quiz.objects.create(**validated_data)
    
    
class QuizViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = ['id','topic','total_marks']
    
           
class AttemptQuizSerializer(serializers.ModelSerializer):
    def __init__(self,*args,**kwargs):
        many = kwargs.pop('many',True)
        super(AttemptQuizSerializer,self).__init__(many=many,*args,**kwargs)
        
    OPTIONS = (
        ('1','Option 1'),
        ('2','Option 2'),
        ('3','Option 3'),
        ('4','Option 4'),

    )
    
    question = serializers.IntegerField()
    answer = serializers.ChoiceField(choices=OPTIONS,required=True)
    class Meta:
        model = Answer
        fields = ['question','answer']
    
