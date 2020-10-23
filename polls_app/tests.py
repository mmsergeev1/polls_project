from django.contrib.auth.models import User
from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.utils import timezone
from .models import Question
import datetime


def create_question(question_text, days, days_till_expiration):
    time = timezone.now() + datetime.timedelta(days=days)
    time_till_expiration = time + datetime.timedelta(days=days_till_expiration)
    return Question.objects.create(question_text=question_text, date_published=time, date_end=time_till_expiration)


class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        """
        If no questions exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse('polls_app:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Нет доступных опросов")
        self.assertQuerysetEqual(response.context['latest_polls_list'], [])

    def test_past_expired_question(self):
        """
        Questions with a pub_date in the past are displayed on the
        index page.
        """
        create_question(question_text="Старый вопрос", days=-30, days_till_expiration=-7)
        response = self.client.get(reverse('polls_app:index'))
        self.assertQuerysetEqual(response.context['latest_polls_list'], [])

    def test_two_past_questions(self):
        """
        The questions index page may display multiple questions.
        """
        create_question(question_text="Старый вопрос 1.", days=-30, days_till_expiration=-7)
        create_question(question_text="Старый вопрос 2.", days=-5, days_till_expiration=-7)
        response = self.client.get(reverse('polls_app:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Нет доступных опросов")
        self.assertQuerysetEqual(response.context['latest_polls_list'], [])

    def test_currently_active_poll(self):
        """
        The questions index page may display multiple questions.
        """
        create_question(question_text="Активный опрос", days=-5, days_till_expiration=7)
        response = self.client.get(reverse('polls_app:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Активные опросы:")
        self.assertQuerysetEqual(response.context['latest_polls_list'], ['<Question: Активный опрос>'])
