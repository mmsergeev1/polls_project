from django.urls import path
from . import views


urlpatterns = [
    path("statistic/<int:pk>", views.RegisteredVoteDetailView.as_view(), name='statistic')
]
