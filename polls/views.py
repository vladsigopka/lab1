from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.views import LoginView
from .models import Question, Choice, User
from django.template import loader
from django.urls import reverse
from django.views import generic
from .forms import UserRegistrationForm, UserUpdateForm
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.forms import formset_factory


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password'])
            new_user.avatar = form.cleaned_data['avatar']
            new_user.save()
            return render(request, 'usermanagment/register_done.html', {'new_user': new_user})
    else:
        form = UserRegistrationForm()

    return render(request, 'usermanagment/register.html', {'form': form})


def update_user(request):
    current_user = request.user
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, request.FILES, instance=current_user)
        if form.is_valid():
            current_user.avatar = form.cleaned_data['avatar']
            form.save()
            return render(request, 'usermanagment/update_done.html')
    else:
        form = UserUpdateForm(initial={'avatar': request.user.avatar.url, 'full_name': request.user.full_name,
                                       'username': request.user.username, 'email': request.user.email})
    return render(request, 'usermanagment/user_update.html', {'form': form})


@login_required
def my_profile(request):
    current_user = request.user
    return render(request, 'usermanagment/my_profile.html', {'user': current_user})


@login_required
def UserDelete(request):
    request.user.delete()
    return render(request, 'usermanagment/user_deleted.html')



def all_q(request):
    questions = Question.objects.all()
    return render(request, 'polls/all_q.html', context={'questions': questions})


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


# @login_required
# def vote(request, question_id):
#     if Question.objects.filter(pk=question_id, voted_by=request.user):
#         return render(request, 'vote_error.html')
#
#     else:
#         question = get_object_or_404(Question, pk=question_id)
#
#         try:
#             selected_choice = question.choice_set.get(pk=request.POST['choice'])
#         except (KeyError, Choice.DoesNotExist):
#             return render(request, 'polls/detail.html', {
#                 'question': question,
#                 'error_message': 'вы не сделали выбор'
#             })
#         else:
#             selected_choice.votes += 1
#             selected_choice.save()
#             return HttpResponseRedirect(reverse('results', args=(question.id,)))

def vote(request, question_id):
    if Question.objects.filter(id=question_id, voted_by=request.user):
        return render(request, 'errors/vote_error.html')

    else:

        question = get_object_or_404(Question, pk=question_id)

        try:
            selected_choice = question.choice_set.get(pk=request.POST['choice'])
        except (KeyError, Choice.DoesNotExist):
            return render(request, 'polls/detail.html', {
                'question': question,
                'error_message': 'вы не сделали выбор'
            })
        else:
            current_q = Question.objects.get(id=question_id)
            current_q.voted_by.add(request.user)
            current_q.votes += 1
            current_q.save()
            selected_choice.votes += 1
            selected_choice.save()
            return HttpResponseRedirect(reverse('results', args=(question.id,)))


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        return Question.objects.all()
