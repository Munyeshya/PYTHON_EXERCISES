from django.db import models
from django.urls import reverse
from django.utils import timezone


class Poll(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    cover_image = models.URLField(blank=True)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField()
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("polls:poll-detail", kwargs={"pk": self.pk})

    @property
    def total_votes(self):
        return self.votes.count()

    @property
    def is_active(self):
        now = timezone.now()
        return self.is_published and self.start_date <= now <= self.end_date


class Choice(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name="choices")
    text = models.CharField(max_length=255)
    votes = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]
        unique_together = ("poll", "text")

    def __str__(self):
        return f"{self.poll.title} - {self.text}"


class Vote(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name="votes")
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE, related_name="votes")
    roll_number = models.CharField(max_length=50)
    voted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-voted_at"]
        constraints = [
            models.UniqueConstraint(fields=["poll", "roll_number"], name="unique_poll_roll_number")
        ]

    def __str__(self):
        return f"{self.roll_number} - {self.poll.title}"
