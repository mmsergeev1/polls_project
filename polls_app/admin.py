from django.contrib import admin
from .models import Question, Choice


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 2


class QuestionAdmin(admin.ModelAdmin):
    readonly_fields = ['date_published']
    fieldsets = [
        (None,               {'fields': ['question_text', 'answer_type']}),
        ('Информация о дате', {'fields': ['date_published', 'date_end'], 'classes': ['collapse']}),
    ]
    inlines = [ChoiceInline]
    list_display = ['question_text', 'date_end', 'answer_type']


admin.site.register(Question, QuestionAdmin)
