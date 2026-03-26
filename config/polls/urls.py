from django.urls import path

from . import views

app_name = "polls"
urlpatterns = [
    path("", views.PollListView.as_view(), name="poll-list"),
    path("polls/<int:pk>/", views.PollDetailView.as_view(), name="poll-detail"),
    path("polls/<int:pk>/results/", views.PollResultsView.as_view(), name="poll-results"),
    path("polls/<int:pk>/vote/", views.vote, name="poll-vote"),
    path("portal/login/", views.admin_login_view, name="admin-login"),
    path("portal/logout/", views.admin_logout_view, name="admin-logout"),
    path("portal/", views.admin_dashboard_view, name="admin-dashboard"),
    path("portal/polls/create/", views.admin_poll_create_view, name="admin-poll-create"),
    path("portal/polls/<int:pk>/", views.admin_poll_detail_view, name="admin-poll-detail"),
    path("portal/polls/<int:pk>/edit/", views.admin_poll_update_view, name="admin-poll-update"),
    path("portal/polls/<int:pk>/delete/", views.admin_poll_delete_view, name="admin-poll-delete"),
    path("portal/polls/<int:poll_pk>/choices/create/", views.admin_choice_create_view, name="admin-choice-create"),
    path("portal/choices/<int:pk>/edit/", views.admin_choice_update_view, name="admin-choice-update"),
    path("portal/choices/<int:pk>/delete/", views.admin_choice_delete_view, name="admin-choice-delete"),
]
