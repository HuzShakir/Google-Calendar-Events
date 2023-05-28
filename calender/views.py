from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Calender
from .serializers import CalenderSerializer
import google_auth_oauthlib.flow
from google.oauth2.credentials import Credentials
import datetime
from googleapiclient.discovery import build
from django.conf import settings
from django.shortcuts import HttpResponseRedirect


class GoogleCalendarRedirectView(APIView):

    def get(self, request, *args, **kwargs):

        flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
            settings.CLIENT_SECRETS_FILE, scopes=["https://www.googleapis.com/auth/calendar.readonly"])
        flow.redirect_uri = f"{settings.SITE_URL}/rest/v1/calendar/redirect"

        authorization_response = request.build_absolute_uri()
        flow.fetch_token(authorization_response=authorization_response)
        credentials = flow.credentials

        calendar = list_events(credentials.token)
        # calendar=list_events("ya29.a0AWY7Ckm0iNxTAhx5ejnxb0acNJOKoE5HQOxQx1_e5vBLn1O39qRIR_qWUvjMCK9j4jLSHpxo1loMCChJZiLotqbUgjMIDqmykPatChJemYr9_7OSJeWH145ebyLySaX1WojWatrUCJ96m9O7dcR3sk9Z0KXqaCgYKASwSARISFQG1tDrpop19elqbavSYFBJLHo9a0g0163")

        serializer = CalenderSerializer(calendar, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


def list_events(access_token):
    creds = Credentials(access_token)
    service = build('calendar', 'v3', credentials=creds)
    now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                          maxResults=100, singleEvents=True,
                                          ).execute()
    events = events_result.get('items', [])
    if not events:
        print('No upcoming events found.')
    calendar = []
    for event in events:
        # start = event['start'].get('dateTime', event['start'].get('date'))
        # print(f'{event["summary"]} ({start})')
        calendar.append(Calender(event=event['summary']))
    return calendar


class GoogleCalendarInitView(APIView):

    def get(self, request, *args, **kwargs):
        flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
            settings.CLIENT_SECRETS_FILE, scopes=["https://www.googleapis.com/auth/calendar.readonly"])
        flow.redirect_uri = f"{settings.SITE_URL}/rest/v1/calendar/redirect"
        authorization_url, state = flow.authorization_url(
            access_type='offline',
            )
        print(authorization_url)
        return HttpResponseRedirect(authorization_url)
