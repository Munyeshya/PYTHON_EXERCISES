from django.urls import path

from . import views

app_name = "polls"
urlpatterns = [
    path("", views.PollListView.as_view(), name="poll-list"),
    path("polls/<int:pk>/", views.PollDetailView.as_view(), name="poll-detail"),
    path("polls/<int:pk>/results/", views.PollResultsView.as_view(), name="poll-results"),
    path("polls/<int:pk>/vote/", views.vote, name="poll-vote"),
]
