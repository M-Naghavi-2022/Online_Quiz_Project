from django.contrib import admin
from .models import Category, Question, Quiz, QuizItem

admin.site.register(Category)
admin.site.register(Question)
admin.site.register(Quiz)
admin.site.register(QuizItem)