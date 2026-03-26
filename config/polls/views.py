from datetime import datetime, timedelta

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import user_passes_test
from django.db.models import F
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_http_methods, require_POST
from django.views.generic import DetailView, ListView

from .models import Choice, Poll, Vote


def superuser_required(view_func):
    return user_passes_test(
        lambda user: user.is_authenticated and user.is_active and user.is_superuser,
        login_url="polls:admin-login",
    )(view_func)


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


@require_http_methods(["GET", "POST"])
def admin_login_view(request):
    if request.user.is_authenticated and request.user.is_superuser:
        return redirect("polls:admin-dashboard")

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")
        user = authenticate(request, username=username, password=password)

        if user and user.is_active and user.is_superuser:
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}.")
            return redirect(request.POST.get("next") or "polls:admin-dashboard")

        messages.error(request, "Enter valid superuser credentials to access the admin portal.")

    return render(request, "polls_admin/login.html", {"next": request.GET.get("next", "")})


@superuser_required
def admin_logout_view(request):
    logout(request)
    messages.success(request, "You have been signed out of the custom admin portal.")
    return redirect("polls:admin-login")


@superuser_required
def admin_dashboard_view(request):
    polls = Poll.objects.prefetch_related("choices").order_by("-created_at")
    context = {
        "polls": polls,
        "poll_count": polls.count(),
        "choice_count": Choice.objects.count(),
        "vote_count": Vote.objects.count(),
        "recent_votes": Vote.objects.select_related("poll", "choice").order_by("-voted_at")[:8],
    }
    return render(request, "polls_admin/dashboard.html", context)


@superuser_required
@require_http_methods(["GET", "POST"])
def admin_poll_create_view(request):
    initial = {
        "start_date": timezone.localtime().strftime("%Y-%m-%dT%H:%M"),
        "end_date": timezone.localtime(timezone.now() + timedelta(days=7)).strftime("%Y-%m-%dT%H:%M"),
        "is_published": True,
    }

    if request.method == "POST":
        title = request.POST.get("title", "").strip()
        description = request.POST.get("description", "").strip()
        cover_image = request.POST.get("cover_image", "").strip()
        start_date_raw = request.POST.get("start_date", "").strip()
        end_date_raw = request.POST.get("end_date", "").strip()
        is_published = request.POST.get("is_published") == "on"
        context = {"page_title": "Create Poll", "form_data": request.POST}

        if not all([title, description, start_date_raw, end_date_raw]):
            messages.error(request, "Title, description, start date, and end date are required.")
            return render(request, "polls_admin/poll_form.html", context)

        try:
            start_date = timezone.make_aware(datetime.fromisoformat(start_date_raw))
            end_date = timezone.make_aware(datetime.fromisoformat(end_date_raw))
        except ValueError:
            messages.error(request, "Enter valid start and end date values.")
            return render(request, "polls_admin/poll_form.html", context)

        if end_date <= start_date:
            messages.error(request, "End date must be later than the start date.")
            return render(request, "polls_admin/poll_form.html", context)

        poll = Poll.objects.create(
            title=title,
            description=description,
            cover_image=cover_image,
            start_date=start_date,
            end_date=end_date,
            is_published=is_published,
        )
        messages.success(request, "Poll created successfully in the custom admin portal.")
        return redirect("polls:admin-poll-detail", pk=poll.pk)

    return render(request, "polls_admin/poll_form.html", {"page_title": "Create Poll", "form_data": initial})


@superuser_required
def admin_poll_detail_view(request, pk):
    poll = get_object_or_404(Poll.objects.prefetch_related("choices", "votes"), pk=pk)
    votes = Vote.objects.filter(poll=poll).select_related("choice").order_by("-voted_at")
    return render(
        request,
        "polls_admin/poll_detail.html",
        {"poll": poll, "votes": votes, "total_votes_safe": poll.total_votes or 1},
    )


@superuser_required
@require_http_methods(["GET", "POST"])
def admin_poll_update_view(request, pk):
    poll = get_object_or_404(Poll, pk=pk)

    if request.method == "POST":
        title = request.POST.get("title", "").strip()
        description = request.POST.get("description", "").strip()
        cover_image = request.POST.get("cover_image", "").strip()
        start_date_raw = request.POST.get("start_date", "").strip()
        end_date_raw = request.POST.get("end_date", "").strip()
        is_published = request.POST.get("is_published") == "on"
        context = {"page_title": "Edit Poll", "poll": poll, "form_data": request.POST}

        if not all([title, description, start_date_raw, end_date_raw]):
            messages.error(request, "Title, description, start date, and end date are required.")
            return render(request, "polls_admin/poll_form.html", context)

        try:
            start_date = timezone.make_aware(datetime.fromisoformat(start_date_raw))
            end_date = timezone.make_aware(datetime.fromisoformat(end_date_raw))
        except ValueError:
            messages.error(request, "Enter valid start and end date values.")
            return render(request, "polls_admin/poll_form.html", context)

        if end_date <= start_date:
            messages.error(request, "End date must be later than the start date.")
            return render(request, "polls_admin/poll_form.html", context)

        poll.title = title
        poll.description = description
        poll.cover_image = cover_image
        poll.start_date = start_date
        poll.end_date = end_date
        poll.is_published = is_published
        poll.save()
        messages.success(request, "Poll updated successfully.")
        return redirect("polls:admin-poll-detail", pk=poll.pk)

    form_data = {
        "title": poll.title,
        "description": poll.description,
        "cover_image": poll.cover_image,
        "start_date": timezone.localtime(poll.start_date).strftime("%Y-%m-%dT%H:%M"),
        "end_date": timezone.localtime(poll.end_date).strftime("%Y-%m-%dT%H:%M"),
        "is_published": poll.is_published,
    }
    return render(
        request,
        "polls_admin/poll_form.html",
        {"page_title": "Edit Poll", "poll": poll, "form_data": form_data},
    )


@superuser_required
@require_POST
def admin_poll_delete_view(request, pk):
    poll = get_object_or_404(Poll, pk=pk)
    poll.delete()
    messages.success(request, "Poll deleted successfully.")
    return redirect("polls:admin-dashboard")


@superuser_required
@require_http_methods(["GET", "POST"])
def admin_choice_create_view(request, poll_pk):
    poll = get_object_or_404(Poll, pk=poll_pk)

    if request.method == "POST":
        text = request.POST.get("text", "").strip()
        if not text:
            messages.error(request, "Choice text is required.")
            return render(request, "polls_admin/choice_form.html", {"page_title": "Add Choice", "poll": poll, "choice_value": text})

        if poll.choices.filter(text__iexact=text).exists():
            messages.error(request, "That choice already exists for this poll.")
            return render(request, "polls_admin/choice_form.html", {"page_title": "Add Choice", "poll": poll, "choice_value": text})

        Choice.objects.create(poll=poll, text=text)
        messages.success(request, "Choice added successfully.")
        return redirect("polls:admin-poll-detail", pk=poll.pk)

    return render(request, "polls_admin/choice_form.html", {"page_title": "Add Choice", "poll": poll})


@superuser_required
@require_http_methods(["GET", "POST"])
def admin_choice_update_view(request, pk):
    choice = get_object_or_404(Choice.objects.select_related("poll"), pk=pk)

    if request.method == "POST":
        text = request.POST.get("text", "").strip()
        if not text:
            messages.error(request, "Choice text is required.")
            return render(request, "polls_admin/choice_form.html", {"page_title": "Edit Choice", "poll": choice.poll, "choice": choice, "choice_value": text})

        if choice.poll.choices.exclude(pk=choice.pk).filter(text__iexact=text).exists():
            messages.error(request, "That choice already exists for this poll.")
            return render(request, "polls_admin/choice_form.html", {"page_title": "Edit Choice", "poll": choice.poll, "choice": choice, "choice_value": text})

        choice.text = text
        choice.save(update_fields=["text"])
        messages.success(request, "Choice updated successfully.")
        return redirect("polls:admin-poll-detail", pk=choice.poll.pk)

    return render(
        request,
        "polls_admin/choice_form.html",
        {"page_title": "Edit Choice", "poll": choice.poll, "choice": choice, "choice_value": choice.text},
    )


@superuser_required
@require_POST
def admin_choice_delete_view(request, pk):
    choice = get_object_or_404(Choice.objects.select_related("poll"), pk=pk)
    poll_pk = choice.poll.pk
    choice.delete()
    messages.success(request, "Choice deleted successfully.")
    return redirect("polls:admin-poll-detail", pk=poll_pk)


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
