from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.utils import timezone
from django.urls import reverse
from django.views import generic
from .models import Question, Choice


class IndexView(generic.ListView):
    template_name = 'polls_app/index.html'
    context_object_name = 'latest_polls_list'

    def get_queryset(self):
        return Question.objects.filter(
            date_published__lte=timezone.now()
        ).order_by('-date_published')[:5]


class DetailsView(generic.DetailView):
    model = Question
    template_name = 'polls_app/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls_app/results.html'


def vote(request, question_id):
    poll = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = poll.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls_app/detail.html', {
            'question': poll,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls_app:results', args=(poll.id,)))
