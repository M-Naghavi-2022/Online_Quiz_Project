import json
from datetime import datetime
from typing import List, Dict

from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from user.models import Profile
from .models import Category, Question, Quiz, QuizItem


class CategoryListView(View):

    def get(self, request):
        category_list = list(Category.objects.values("name"))
        return JsonResponse(category_list, safe=False)



@method_decorator(csrf_exempt, name= 'dispatch')
class GenerateQuizView(View):

    GENERATE_DATA_FIELDS = ["username", "category"]

    def _is_valid_data(self, data: Dict):
        result = {"error": False}
        for field in GenerateQuizView.GENERATE_DATA_FIELDS:
            if field not in data.keys():
                result.update({"error" : True})
                result["error_message"] = f"{field} field is required"
                return result
        return result

    def post(self, request):
        try:
            data = json.loads(request.body)
        except:
            return JsonResponse({'status':'false','message':"Please send your request in Json"}, status=400)
        if self._is_valid_data(data)["error"]:
            return JsonResponse(self._is_valid_data(data), status=400)

        user: Profile = get_object_or_404(Profile, username=data.get("username"))
        if Quiz.objects.filter(user=user , done=False):
            return JsonResponse({'status':'false','message':"You have an uncompleted quiz, Please answer it first!!!"})

        categories_str: List = data.get("category")
        categories_obj = []
        for elm in categories_str:
            categories_obj.append(get_object_or_404(Category, name= elm))
        
        total_question_number = 15 
        categories_questions_number = {}
        for elm in categories_str:
            categories_questions_number[elm] = total_question_number//len(categories_str)
        if total_question_number%len(categories_str) != 0:
            res = total_question_number%len(categories_str)
            for i in range(res):
                categories_questions_number[categories_str[i]] += 1

        quiz_obj: Quiz = Quiz.objects.create(user = user)
        quiz = {"username": user.username, "quiz_number": quiz_obj.id}
        quiz_correct_answers = {}
        quiz_question_number = 1
        for elm in categories_obj:
            qs = Question.objects.filter(category = elm)\
                .order_by('?')[:categories_questions_number[elm.name]]
            for q in qs:
                QuizItem.objects.create(quiz = quiz_obj, question = q, quiz_related_number = quiz_question_number)
                quiz[f'{quiz_question_number}({elm.name})'] = {
                    "question": q.question,
                    "choice_a": q.choice_a,
                    "choice_b": q.choice_b,
                    "choice_c": q.choice_c,
                    "choice_d": q.choice_d
                }
                quiz_correct_answers[quiz_question_number] = q.correct_answer
                quiz_question_number += 1
        quiz_obj.correct_answers = quiz_correct_answers
        quiz_obj.save()

        return JsonResponse(quiz)



@method_decorator(csrf_exempt, name= 'dispatch')
class AnswerQuizView(View):
    GENERATE_DATA_FIELDS = ["username", "quiz_number"]

    def _is_valid_data(self, data: Dict):
        result = {"error": False}
        for field in AnswerQuizView.GENERATE_DATA_FIELDS:
            if field not in data.keys():
                result.update({"error" : True})
                result["error_message"] = f"{field} field is required"
                return result
        return result

    def post(self, request):
        try:
            data: Dict = json.loads(request.body)
        except:
            return JsonResponse({'status':'false','message':"Please send your answer in Json"}, status=400)
        if self._is_valid_data(data)["error"]:
            return JsonResponse(self._is_valid_data(data), status=400)

        user: Profile = get_object_or_404(Profile, username=data.get("username"))
        del data['username']

        quiz_obj: Quiz = get_object_or_404(Quiz, id=data.get("quiz_number"))
        del data['quiz_number']

        if quiz_obj.user != user:
            return JsonResponse({'status':'false','message':"This quiz was not assigned to you, You are not allowed to answer it"}, status=400)
        if quiz_obj.done:
            return JsonResponse({'status':'false','message':"You have already answered this quiz and cannot answer it more than once, please requst a new one to answer!"}, status=400)

        for i in data.keys():

            quiz_item_obj: QuizItem = get_object_or_404(QuizItem, quiz= quiz_obj.id, quiz_related_number=i)
            quiz_item_obj.user_answer = data.get(f"{i}")

            if  quiz_item_obj.user_answer == quiz_obj.correct_answers[f"{i}"]:
                quiz_obj.result['total_score'] += 3
                quiz_obj.result['correct_ans'] += 1                
            else:
                quiz_obj.result['total_score'] -= 1
                quiz_obj.result['wrong_ans'] += 1
            quiz_item_obj.save()

        quiz_obj.result['blank_ans'] += QuizItem.objects.filter(quiz= quiz_obj, user_answer= None).count()
        quiz_obj.done = True
        quiz_obj.completion_date = datetime.now()
        quiz_obj.save()

        quiz_result = {"username": user.username, "quiz_number": quiz_obj.id, "quiz_result":quiz_obj.result}
        return JsonResponse(quiz_result)



@method_decorator(csrf_exempt, name= 'dispatch')
class QuizHistoryView(View):
    
    def post(self, request):
        try:
            data = json.loads(request.body)
        except:
            return JsonResponse({'status':'false','message':"Please send your request in Json"}, status=400)
        if 'username' not in data.keys():
            return JsonResponse({'status':'false','message':"Please include your username in the Json"}, status=400)

        user: Profile = get_object_or_404(Profile, username=data.get("username"))
        quiz_history = Quiz.objects.filter(user=user).values('id','generation_request_date','done','completion_date','result')
        quiz_history = list(quiz_history)
        return JsonResponse({'username':user.username, 'quiz_history':quiz_history})