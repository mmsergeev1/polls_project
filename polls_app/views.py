from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.utils import timezone
from django.urls import reverse
from django.views import generic

import polls_app
from polls_app.models import Question, Choice, RegisteredVote
import logging


logging.basicConfig(filename='app.log', filemode='a', format='%(name)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG)


class IndexView(generic.ListView):
    template_name = 'polls_app/index.html'
    context_object_name = 'latest_polls_list'

    def get_queryset(self):
        return Question.objects.all().filter(date_published__lte=timezone.now(), date_end__gte=timezone.now())


class DetailsView(generic.DetailView):
    model = Question
    template_name = 'polls_app/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls_app/results.html'


def vote(request, question_id):
    poll = get_object_or_404(Question, pk=question_id)
    logging.debug(f'answer type = {poll.answer_type}')
    if poll.answer_type == 'CH':
        try:
            selected_choice = poll.choice_set.get(pk=request.POST['choice'])
            logging.debug(f'selected_choice = {selected_choice.votes}')
            logging.debug(f"request: {request.POST}")
            selected_choice.votes += 1
            selected_choice.save()
            if request.user.is_authenticated:
                registered_vote = RegisteredVote.objects.create(question=poll,
                                                                choice=selected_choice,
                                                                user=request.user)
                registered_vote.save()
            else:
                registered_vote = RegisteredVote.objects.create(question=poll,
                                                                choice=selected_choice,
                                                                anonymous_user_id=int(request.POST['user_id']))
                registered_vote.save()
            return HttpResponseRedirect(reverse('polls_app:results', args=(poll.id,)))
        except (KeyError, Choice.DoesNotExist):
            return render(request, 'polls_app/detail.html', {
                'question': poll,
                'error_message': "Выбор не распознан",
            })
    elif poll.answer_type == 'TE':
        logging.debug(f"request: {request.POST}")
        try:
            selected_choice = poll.choice_set.get(choice=request.POST['choice'])
            selected_choice.votes += 1
            selected_choice.save()
            if request.user.is_authenticated:
                registered_vote = RegisteredVote.objects.create(question=poll,
                                                                choice=selected_choice,
                                                                user=request.user)
                registered_vote.save()
            else:
                registered_vote = RegisteredVote.objects.create(question=poll,
                                                                choice=selected_choice,
                                                                anonymous_user_id=int(request.POST['user_id']))
                registered_vote.save()
        except polls_app.models.Choice.DoesNotExist:
            poll.choice_set.create(votes=1,
                                   choice=request.POST['choice'])
            selected_choice = poll.choice_set.get(choice=request.POST['choice'])
            if request.user.is_authenticated:
                registered_vote = RegisteredVote.objects.create(question=poll,
                                                                choice=selected_choice,
                                                                user=request.user)
                registered_vote.save()
            else:
                registered_vote = RegisteredVote.objects.create(question=poll,
                                                                choice=selected_choice,
                                                                anonymous_user_id=int(request.POST['user_id']))
                registered_vote.save()
        return HttpResponseRedirect(reverse('polls_app:results', args=(poll.id,)))
    elif poll.answer_type == 'MU':
        logging.debug(f"request: {request.POST}")
        try:
            for item in request.POST.getlist('choice'):
                logging.debug(f"item: {item}, request.post.choice = {request.POST.getlist('choice')}")
                selected_choice = poll.choice_set.get(pk=item)
                selected_choice.votes += 1
                selected_choice.save()
                if request.user.is_authenticated:
                    registered_vote = RegisteredVote.objects.create(question=poll,
                                                                    choice=selected_choice,
                                                                    user=request.user)
                    registered_vote.save()
                else:
                    registered_vote = RegisteredVote.objects.create(question=poll,
                                                                    choice=selected_choice,
                                                                    anonymous_user_id=int(request.POST['user_id']))
                    registered_vote.save()
            return HttpResponseRedirect(reverse('polls_app:results', args=(poll.id,)))
        except (KeyError, Choice.DoesNotExist):
            return render(request, 'polls_app/detail.html', {
                'question': poll,
                'error_message': "Выбор не распознан",
            })
