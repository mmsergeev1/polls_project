from django.contrib.auth.models import User
from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.utils import timezone
from .models import Question
import datetime


def create_question(question_text, days, days_till_expiration):
    """
    Создание опроса с указанными параметрами
    :param question_text: Текст опроса
    :param days: Дней до создания запроса, больше нуля будущее, меньше - прошлое
    :param days_till_expiration: Дней до истечения срока жизни опроса, больше нуля будущее, меньше - прошлое
    :return: Опрос с указанными параматрами
    """
    time = timezone.now() + datetime.timedelta(days=days)
    time_till_expiration = time + datetime.timedelta(days=days_till_expiration)
    return Question.objects.create(question_text=question_text, date_published=time, date_end=time_till_expiration)


class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        """
        Тест-кейс 1: нет никаких опросов в базе, никаких данных не должно выводиться
        """
        response = self.client.get(reverse('polls_app:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Нет доступных опросов")
        self.assertQuerysetEqual(response.context['latest_polls_list'], [])

    def test_expired_question(self):
        """
        Тест-кейс 2: в базе только просроченный опрос, никаких данных не должно выводиться
        """
        create_question(question_text="Старый вопрос", days=-30, days_till_expiration=-7)
        response = self.client.get(reverse('polls_app:index'))
        self.assertQuerysetEqual(response.context['latest_polls_list'], [])

    def test_two_past_questions(self):
        """
        Тест-кейс 3: в базе несколько просроченных запросов, никаких данных не должно выводиться
        """
        create_question(question_text="Старый вопрос 1.", days=-30, days_till_expiration=-7)
        create_question(question_text="Старый вопрос 2.", days=-5, days_till_expiration=-7)
        response = self.client.get(reverse('polls_app:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Нет доступных опросов")
        self.assertQuerysetEqual(response.context['latest_polls_list'], [])

    def test_currently_active_poll(self):
        """
        Тест-кейс 4: в базе один активный опрос, должен вернуться этот опрос
        """
        create_question(question_text="Активный опрос", days=-5, days_till_expiration=7)
        response = self.client.get(reverse('polls_app:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Активные опросы:")
        self.assertQuerysetEqual(response.context['latest_polls_list'], ['<Question: Активный опрос>'])
