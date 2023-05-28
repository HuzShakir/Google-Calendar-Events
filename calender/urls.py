from django.urls import path, include
from .views import GoogleCalendarRedirectView,GoogleCalendarInitView

urlpatterns = [
    path('init', GoogleCalendarInitView.as_view()),
    path('redirect', GoogleCalendarRedirectView.as_view()),
]