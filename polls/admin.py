from django.contrib import admin
from .models import Question, Choice, User


class ChoiceInLine(admin.TabularInline):
    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInLine]
    readonly_fields = ['votes', 'voted_by', 'id']


admin.site.register(Question, QuestionAdmin)
admin.site.register(User)
admin.site.register(Choice)

