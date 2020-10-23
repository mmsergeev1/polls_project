from datetime import timedelta
from django.db import models
from django.utils import timezone


class Question(models.Model):
    text_field = 'TE'
    choice_field = 'CH'
    multiple_choice_field = 'MU'
    answer_types = [
        (text_field, 'Текстовый ответ'),
        (choice_field, 'Выбор ответа'),
        (multiple_choice_field, 'Выбор нескольких ответов'),
    ]

    question_text = models.CharField('Текст вопроса', max_length=200)
    date_published = models.DateTimeField('Дата публикации', editable=False)
    date_end = models.DateTimeField('Дата окончания', default=timezone.now() + timedelta(7))
    answer_type = models.CharField('Тип ответа', max_length=2, choices=answer_types, default=text_field)

    def __str__(self):
        return self.question_text

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    votes = models.IntegerField(default=0)
    choice = models.CharField(max_length=200)

    def __str__(self):
        return self.choice

    class Meta:
        verbose_name = 'Голос'
        verbose_name_plural = 'Голоса'
