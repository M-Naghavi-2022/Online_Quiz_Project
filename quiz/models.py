from django.db import models

from user.models import Profile


class Category(models.Model):
    name = models.CharField(max_length= 50)

    def __str__(self) -> str:
        return self.name


class Question(models.Model):
    ANSWERS = [
        ('a','choice a'),
        ('b','choice b'),
        ('c','choice c'),
        ('d','choice d')
    ]
    question = models.CharField(max_length= 255)
    choice_a = models.CharField(max_length= 100)
    choice_b = models.CharField(max_length= 100)
    choice_c = models.CharField(max_length= 100)
    choice_d = models.CharField(max_length= 100)
    correct_answer = models.CharField(max_length= 1, choices= ANSWERS)
    category = models.ForeignKey(Category, on_delete= models.RESTRICT)
    creation_date = models.DateTimeField(auto_now_add= True)

    def __str__(self) -> str:
        return f'{self.question} / {self.category.name}'


class Quiz(models.Model):
    user = models.ForeignKey(Profile, on_delete= models.CASCADE)
    generation_request_date = models.DateTimeField(auto_now_add= True)
    done = models.BooleanField(default= False)
    completion_date = models.DateTimeField(null= True, blank= True)
    correct_answers = models.JSONField(default= dict())
    result = models.JSONField(default= {'total_score': 0, 'correct_ans': 0, 'wrong_ans' : 0, 'blank_ans' : 0})

    def __str__(self) -> str:
        return f'{self.user} @ {self.generation_request_date}'


class QuizItem(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete= models.CASCADE)
    quiz_related_number = models.SmallIntegerField(default= 1)
    question = models.ForeignKey(Question, on_delete= models.CASCADE)
    user_answer = models.CharField(max_length=1, null= True, blank= True)

    def __str__(self) -> str:
        return f'{self.quiz} / Q{self.quiz_related_number}'
