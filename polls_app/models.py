from datetime import timedelta
from django.contrib.auth.models import User
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

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'

    def __str__(self):
        return self.question_text

    def save(self, new_image=False, *args, **kwargs):
        if not self.id:
            self.date_published = timezone.now()
        super(Question, self).save(*args, **kwargs)


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    votes = models.IntegerField('Количество голосов', default=0)
    choice = models.CharField('Выбранный вариант ответа', max_length=200)

    def __str__(self):
        return self.choice

    class Meta:
        verbose_name = 'Голос'
        verbose_name_plural = 'Голоса'


class RegisteredVote(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    anonymous_user_id = models.IntegerField('Айди анонимного пользователя', null=True, blank=True)
