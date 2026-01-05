from django.db.models import F
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .models import Choice, Question


class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """Возвращает 5 последних опубликованных вопросов 
        (исключая запланированные к публикации)"""
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[:5]

#def index(request):
#    latest_question_list = Question.objects.order_by("-pub_date")[:5]
#    #v 3.1
#    #output = ", ".join([q.question_text for q in latest_question_list])
#    context = {
#        "latest_question_list": latest_question_list,
#    }
#    #v 3.1
#    #return HttpResponse(output)
#    return render(request, "polls/index.html", context)


class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"

#def detail(request, question_id):
#    #Вариант обработки ошибки 404 с помощью Shortcuts
#    question = get_object_or_404(Question, pk=question_id)
#
#    # Вариант обработки ошибки 404 с помощью raise
#    try:
#        question = Question.objects.get(pk=question_id)
#    except Question.DoesNotExist:
#        raise Http404("Question does not exist")
#    
#    return render(request, "polls/detail.html", {"question":question})

class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"

#def results(request, question_id):
#    question = get_object_or_404(Question, pk=question_id)
#    return render(request, "polls/results.html", {"question": question})

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # Показать форму снова
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        selected_choice.votes = F("votes") + 1
        selected_choice.save()
        # Возвращай HttpResponseRedirect после каждого изменения, чтобы
        # не сохранять один и тот же ответ дважды, если пользователь
        # нажмет "назад"
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))