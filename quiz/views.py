
# Create your views here.


from django.shortcuts import redirect
from django.db.models import Count
from .models import Question,Quiz,Answer,Result
from account.models import Teacher,Student
from rest_framework.response import Response
from rest_framework import generics
from .serializers import QuestionSerializer,QuizSerializer,AttemptQuizSerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import IsTeacher,IsStudent,NotAttempted,HasAttempted
import ast
# Create your views here.

class DisplayQuizzes(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    
    def get(self,request,*args,**kwargs):
        if request.user.is_student:
            quizzes = list(Quiz.objects.all().values())
        else:
            quizzes = list(Quiz.objects.filter(teacher=request.user).values())
        context = {
            'quizzes' : quizzes
        }
        return Response(context)


class DisplayQuestions(generics.GenericAPIView):
    permission_classes = [IsAuthenticated,IsTeacher]
    
    def get(self,request,*args,**kwargs):
        instance = Quiz.objects.get(id=kwargs['quiz_id'])
        questions = list(Question.objects.filter(quiz=instance).values())
        context = {
            'questions' : questions
        }
        return Response(context)


class CreateInfo(generics.GenericAPIView):
    serializer_class = QuizSerializer
    permission_classes = [IsAuthenticated,IsTeacher]
    
    def post(self,request,*args,**kwargs):
        serializer = QuizSerializer(data=request.data)
        if serializer.is_valid():
            teacher = Teacher.objects.get(email=request.user)
            instance = serializer.save(teacher=teacher)
            return redirect('create',instance.id)
        else:
            return Response(serializer.errors)


class Create(generics.GenericAPIView):
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticated,IsTeacher]
    
    def post(self,request,*args,**kwargs):
        serializer = QuestionSerializer(data=request.data)
        quiz_id = kwargs['quiz_id']
        teacher = Teacher.objects.get(email=request.user)
        instance = Quiz.objects.get(id=quiz_id,teacher=teacher)
        if Question.objects.filter(quiz=instance).aggregate(Count('question_text'))['question_text__count'] >= instance.total_marks:
            return Response({'response':'You have already added '+str(instance.total_marks)+' questions for quiz id : '+str(quiz_id)})
        else:
            if serializer.is_valid():
                correct = serializer.validated_data['correct_choice']
                if correct == '1':
                    serializer.save(correct_choice=serializer.validated_data['choice1'],quiz=instance)
                elif correct == '2':
                    serializer.save(correct_choice=serializer.validated_data['choice2'],quiz=instance)
                elif correct == '3':
                    serializer.save(correct_choice=serializer.validated_data['choice3'],quiz=instance)
                elif correct == '4':
                    serializer.save(correct_choice=serializer.validated_data['choice4'],quiz=instance)
                count = Question.objects.filter(quiz=instance).aggregate(Count('question_text'))['question_text__count'] + 1
                if count < instance.total_marks:
                    context = {
                        'response' : 'Question successfully added',
                        'quiz id' : quiz_id,
                    }
                elif count == instance.total_marks:
                    context = {
                        'response' : 'Question successfully added',
                        'message' : 'Enter last Question of the quiz',
                        'quiz id' : quiz_id
                    }
                else:
                    return redirect('display_questions',quiz_id)
            
                return Response(context)
            else:
                return Response(serializer.errors)
        


class Delete(generics.GenericAPIView):
    permission_classes = [IsAuthenticated,IsTeacher]
    
    def get(self,request,quiz_id=0,question_id=0):
        try:
            if quiz_id != 0:
                Quiz.objects.get(id=quiz_id).delete()
                context = {
                    "response" : "Quiz successfully deleted"
                }
            elif question_id != 0:
                Question.objects.get(id=question_id).delete()
                context = {
                    "response" : "Question successfully deleted"
                }
        except:
            context = {
                "response" : "Please enter a valid id"
            }
        return Response(context)


class UpdateQuestion(generics.GenericAPIView):
    permission_classes = [IsAuthenticated,IsTeacher]
    serializer_class = QuestionSerializer
    
    def post(self,request,*args,**kwargs):
        question = Question.objects.get(id=kwargs['question_id'])
        serializer = QuestionSerializer(question,data=request.data)
        if serializer.is_valid():
            correct = serializer.validated_data['correct_choice']
            if correct == '1':
                serializer.save(correct_choice=serializer.validated_data['choice1'])
            elif correct == '2':
                serializer.save(correct_choice=serializer.validated_data['choice2'])
            elif correct == '3':
                serializer.save(correct_choice=serializer.validated_data['choice3'])
            elif correct == '4':
                serializer.save(correct_choice=serializer.validated_data['choice4'])
            return Response({'response':'Question updated'})
        else:
            return Response(serializer.errors)


class UpdateQuiz(generics.GenericAPIView):
    permission_classes = [IsAuthenticated,IsTeacher]
    serializer_class = QuizSerializer
    
    def post(self,request,*args,**kwargs):
        quiz = Quiz.objects.get(id=kwargs['quiz_id'])
        serializer = QuizSerializer(quiz,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'response':'Quiz updated'})
        else:
            return Response(serializer.errors)




class AttemptQuiz(generics.GenericAPIView):
    permission_classes = [IsAuthenticated,IsStudent,NotAttempted]
    serializer_class = AttemptQuizSerializer
    queryset = Answer.objects.all()
    
    def get(self,request,*args,**kwargs):
        quiz_id = kwargs['quiz_id']
        quiz = Quiz.objects.get(id=quiz_id)
        self.quiz_id = quiz_id
        questions = list(Question.objects.filter(quiz=quiz).values())
        for question in questions:
            question.pop('correct_choice')
        return Response(questions)
        
    def post(self,request,*args,**kwargs):
        serializer = AttemptQuizSerializer(data=request.data,many=True)
        student = Student.objects.get(email=request.user)
        quiz = Quiz.objects.get(id=kwargs['quiz_id'])
        if serializer.is_valid():
            try:
                marks = 0
                for data in serializer.validated_data:
                    question_id = data["question"]
                    option = data["answer"]
                    if option == '1':
                        data["answer"] = Question.objects.get(id=question_id,quiz=quiz).choice1
                    elif option == '2':
                        data["answer"] = Question.objects.get(id=question_id,quiz=quiz).choice2
                    elif option == '3':
                        data["answer"] = Question.objects.get(id=question_id,quiz=quiz).choice3
                    elif option == '4':
                        data["answer"] = Question.objects.get(id=question_id,quiz=quiz).choice4
                    else:
                        return Response({'response':'Please enter a valid option number'})
                    data["question"] = Question.objects.get(id=question_id,quiz=quiz)
                    data["student"] = student
                    if data["answer"] == Question.objects.get(id=question_id,quiz=quiz).correct_choice:
                        marks = marks + 1
                Result.objects.create(student=student,quiz=quiz,marks_obtained=marks)
                print(serializer.validated_data)
                serializer.save()
                return Response({'response':'Quiz attempted successfully'})
            except:
                return Response({'response':'Please enter a valid quiz id'})
        else:
            return Response(serializer.errors)
       
    

class StudentResult(generics.GenericAPIView):
    permission_classes = [IsAuthenticated,HasAttempted]
    queryset = Result.objects.all()
    def get(self,request,*args,**kwargs):
        quiz_id = kwargs["quiz_id"]
        def func(m,n):
            m["answer"] = n["answer"]
            return m
        try:
            if request.user.is_student:
                student = Student.objects.get(email=request.user)
                quiz = Quiz.objects.get(id=quiz_id)
                question_objs = Question.objects.filter(quiz=quiz)
                marks = ast.literal_eval(str(list(Result.objects.filter(student=student,quiz=quiz).values('marks_obtained')))[1:-1])
                print(marks)
                questions = Question.objects.filter(quiz=quiz).values('question_text','correct_choice')
                answers = Answer.objects.filter(student=student,question__in=question_objs).values('answer')
                result = list(map(func,questions,answers))
                result.insert(0,marks)
            else:
                teacher = Teacher.objects.get(email=request.user)
                quiz = Quiz.objects.get(id=quiz_id,teacher=teacher)
                result = list(Result.objects.filter(quiz=quiz).values())
            return Response(result)
        except:
            return Response({'response':'Please enter a valid quiz id'})

