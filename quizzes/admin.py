from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Quiz, Question, Answer, QuizAttempt

class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 4

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'passing_score', 'time_limit']
    list_filter = ['course']
    search_fields = ['title']

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['text', 'quiz', 'points', 'order']
    list_filter = ['quiz']
    search_fields = ['text']
    inlines = [AnswerInline]

@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    list_display = ['user', 'quiz', 'score', 'passed', 'completed_at']
    list_filter = ['passed', 'started_at']
    search_fields = ['user__username', 'quiz__title']