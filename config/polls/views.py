from django.contrib import messages
from django.db.models import F
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from django.views.generic import DetailView, ListView

from .models import Choice, Poll, Vote


class PollListView(ListView):
    model = Poll
    template_name = "polls/poll_list.html"
    context_object_name = "polls"

    def get_queryset(self):
        now = timezone.now()
        return (
            Poll.objects.filter(is_published=True, start_date__lte=now)
            .prefetch_related("choices")
            .order_by("-created_at")
        )


class PollDetailView(DetailView):
    model = Poll
    template_name = "polls/poll_detail.html"
    context_object_name = "poll"

    def get_queryset(self):
        now = timezone.now()
        return Poll.objects.filter(is_published=True, start_date__lte=now).prefetch_related("choices")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_votes_safe"] = self.object.total_votes or 1
        return context


class PollResultsView(DetailView):
    model = Poll
    template_name = "polls/poll_results.html"
    context_object_name = "poll"

    def get_queryset(self):
        now = timezone.now()
        return Poll.objects.filter(is_published=True, start_date__lte=now).prefetch_related("choices")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_votes_safe"] = self.object.total_votes or 1
        return context


def vote(request, pk):
    poll = get_object_or_404(Poll, pk=pk)
    roll_number = request.POST.get("roll_number", "").strip()
    choice_id = request.POST.get("choice")

    if request.method != "POST":
        return redirect(poll.get_absolute_url())

    if not roll_number:
        messages.error(request, "Please enter your roll number before voting.")
        return redirect(poll.get_absolute_url())

    if not choice_id:
        messages.error(request, "Please select an option before submitting your vote.")
        return redirect(poll.get_absolute_url())

    if not poll.is_active:
        messages.error(request, "This poll is not currently accepting votes.")
        return redirect(poll.get_absolute_url())

    choice = get_object_or_404(Choice, pk=choice_id, poll=poll)
    if Vote.objects.filter(poll=poll, roll_number__iexact=roll_number).exists():
        messages.error(request, "This roll number has already been used for this poll.")
        return redirect(poll.get_absolute_url())

    Vote.objects.create(poll=poll, choice=choice, roll_number=roll_number)
    Choice.objects.filter(pk=choice.pk).update(votes=F("votes") + 1)
    messages.success(request, f'Vote recorded for roll number "{roll_number}".')
    return redirect("polls:poll-results", pk=poll.pk)
