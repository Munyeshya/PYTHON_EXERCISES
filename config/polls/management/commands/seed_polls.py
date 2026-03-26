from datetime import timedelta
import random

from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone
from faker import Faker

from polls.models import Choice, Poll, Vote


class Command(BaseCommand):
    help = "Seed the database with fake polls, choices, and votes."

    def add_arguments(self, parser):
        parser.add_argument(
            "--count",
            type=int,
            default=10,
            help="Number of polls to create. Maximum is 15.",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        faker = Faker()
        requested_count = options["count"]
        poll_count = min(max(requested_count, 1), 15)

        created_polls = 0
        created_choices = 0
        created_votes = 0

        for _ in range(poll_count):
            start_date = timezone.now() - timedelta(days=random.randint(0, 5))
            end_date = start_date + timedelta(days=random.randint(3, 14))
            poll = Poll.objects.create(
                title=faker.sentence(nb_words=5).rstrip("."),
                description=faker.paragraph(nb_sentences=3),
                start_date=start_date,
                end_date=end_date,
                is_published=True,
            )
            created_polls += 1

            choices = []
            for _ in range(random.randint(3, 5)):
                choice = Choice.objects.create(
                    poll=poll,
                    text=faker.sentence(nb_words=4).rstrip("."),
                )
                choices.append(choice)
                created_choices += 1

            vote_total = random.randint(4, 16)
            for _ in range(vote_total):
                selected_choice = random.choice(choices)
                Vote.objects.create(
                    poll=poll,
                    choice=selected_choice,
                    roll_number=f"ULK/{faker.unique.random_int(min=10000, max=99999)}",
                )
                selected_choice.votes += 1
                selected_choice.save(update_fields=["votes"])
                created_votes += 1

            faker.unique.clear()

        self.stdout.write(
            self.style.SUCCESS(
                f"Seed complete: {created_polls} polls, {created_choices} choices, {created_votes} votes."
            )
        )
