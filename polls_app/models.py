from django.db import models


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    date_published = models.DateTimeField('Дата публикации')

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
