from django.contrib.auth.models import User
from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.utils import timezone
from .models import Question
import datetime


def create_question(question_text, days):
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, date_published=time)


class QuestionIndexViewTests(TestCase):
    def setUp(self):
        self.client.login(username='test', password='test')
        self.user = User.objects.get(username='test')

    def test_not_logged_on(self):
        """
        If no questions exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse('polls_app:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Для пользования сервисом войдите в личный кабинет.")

    def test_no_questions(self):
        """
        If no questions exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Нет доступных опросов")
        self.assertQuerysetEqual(response.context['latest_polls_list'], [])

    def test_past_question(self):
        """
        Questions with a pub_date in the past are displayed on the
        index page.
        """
        create_question(question_text="Старый вопрос", days=-30)
        response = self.client.get(reverse('polls_app:index'))
        self.assertQuerysetEqual(
            response.context['latest_polls_list'],
            ['<Question: Старый вопрос>']
        )

    def test_future_question(self):
        """
        Questions with a pub_date in the future aren't displayed on
        the index page.
        """
        self.client.login(username='test', password='test')
        create_question(question_text="Вопрос из будущего", days=30)
        response = self.client.get(reverse('polls_app:index'))
        self.assertContains(response, "Нет доступных опросов")
        self.assertQuerysetEqual(response.context['latest_polls_list'], [])

    def test_future_question_and_past_question(self):
        """
        Even if both past and future questions exist, only past questions
        are displayed.
        """
        create_question(question_text="Старый вопрос", days=-30)
        create_question(question_text="Вопрос из будущего", days=30)
        response = self.client.get(reverse('polls_app:index'))
        self.assertQuerysetEqual(
            response.context['latest_polls_list'],
            ['<Question: Старый вопрос>']
        )

    def test_two_past_questions(self):
        """
        The questions index page may display multiple questions.
        """
        create_question(question_text="Старый вопрос 1.", days=-30)
        create_question(question_text="Старый вопрос 2.", days=-5)
        response = self.client.get(reverse('polls_app:index'))
        self.assertQuerysetEqual(
            response.context['latest_polls_list'],
            ['<Question: Старый вопрос 2.>', '<Question: Старый вопрос 1.>']
        )
