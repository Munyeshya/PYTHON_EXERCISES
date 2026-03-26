from django.contrib import admin

from .models import Choice, Poll, Vote


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 1


class VoteInline(admin.TabularInline):
    model = Vote
    extra = 0
    readonly_fields = ("roll_number", "choice", "voted_at")
    can_delete = False
    fields = ("roll_number", "choice", "voted_at")

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):
    list_display = ("title", "is_published", "start_date", "end_date", "total_votes")
    list_filter = ("is_published", "start_date", "end_date")
    search_fields = ("title", "description")
    inlines = [ChoiceInline, VoteInline]


@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ("text", "poll", "votes", "created_at")
    list_filter = ("poll",)
    search_fields = ("text",)


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ("roll_number", "poll", "choice", "voted_at")
    list_filter = ("poll", "choice", "voted_at")
    search_fields = ("roll_number", "poll__title", "choice__text")
    readonly_fields = ("poll", "choice", "roll_number", "voted_at")

    def has_add_permission(self, request):
        return False
