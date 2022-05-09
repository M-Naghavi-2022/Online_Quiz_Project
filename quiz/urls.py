from django.urls import path

from .views import CategoryListView, GenerateQuizView, AnswerQuizView , QuizHistoryView

urlpatterns = [
    path('', CategoryListView.as_view(), name="category_list"),
    path('generate-quiz/', GenerateQuizView.as_view(), name="generate_quiz"),
    path('answer-quiz/', AnswerQuizView.as_view(), name="answer_quiz"),
    path('quiz-history/', QuizHistoryView.as_view(), name="quiz_history"),
]
