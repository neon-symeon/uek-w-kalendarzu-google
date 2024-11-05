import os

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
# from googleapiclient.errors import HttpError

from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings


SCOPES = ['https://www.googleapis.com/auth/calendar']
CREDENTIALS = 'token_json_files/credentials.json'


class GoogleAuthentication(LoginRequiredMixin):
    """
    Obsługuje uwierzytelnienie dostępu do kalendarza Google.
    """

    def __init__(self, user_id: int) -> None:
        """
        user_id potrzebny do identyfikacji tokena dla zalogowanego usera.
        """
        self.user_id = user_id

    def get_service(self):
        """
        Zwraca endpoint serwisowy do kalendarza Google.
        Misja klasy realizuje się w tej metodzie.
        """
        creds = self._get_creds()
        service = build('calendar', 'v3', credentials=creds)
        return service

    def _get_creds(self):
        """
        Zwraca uwierzytelnienie dostępu do kalendarza Google.
        """
        # Personalizowana identyfikacja tokena za pomocą id uzytkownika
        token = f'token_json_files/token_{self.user_id}.json'

        creds = None
        if os.path.exists(token):
            creds = Credentials.from_authorized_user_file(token, SCOPES)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    CREDENTIALS, SCOPES
                )
                creds = flow.run_local_server(port=0)

            with open(token, 'w') as token:
                token.write(creds.to_json())

        return creds


class GoogleCalendarClient(GoogleAuthentication):
    """
    Obsługuje CRUD dla kalendarza Google.
    Aktualnie funkcjonuje Create or Update.

    linki do dokumentacji:
    https://developers.google.com/calendar/api/v3/reference/events
    https://developers.google.com/calendar/api/quickstart/python?hl=pl

    link do obsidiana:
    `/home/simon/Documents/obsidian_new/2024_05_22/google calendar integration with Django.md`
    """

    def __init__(self, user_id: int) -> None:
        super().__init__(user_id=user_id)
        self.service = self.get_service()

    def set_body(self, event: dict) -> dict:
        """
        Creates event body.
        """
        body = {
            # These three is a must:
            'summary': event['summary'],
            'start': {
                'dateTime': event['start'].isoformat(),
                'timeZone': settings.TIME_ZONE
            },
            'end': {
                'dateTime': event['end'].isoformat(),
                'timeZone': settings.TIME_ZONE
            },
            # The rest are optional:
            'location': event['location'],
            'description': event['description'],
            'reminders': {
                'useDefault': False,
            },

        }
        # TODO: add reminders, kolory
        # TODO: add rodzaj kalendarza - wybierany z listy dostępnych kalendarzy.

        return body

    def create_or_update_event(
            self,
            event: dict
    ) -> str:
        """
        Calls the API wih the necessary details
        in order to create or update a google calendar event.
        """
        # Creates event body.
        body = self.set_body(event)

        old_id = self._check_for_update(body)

        print('old_id:', old_id)

        if old_id:
            # Updates existing google event.
            google_event = self.service.events().update(
                calendarId="primary",
                eventId=old_id,
                body=body
            ).execute()

            if google_event:
                print(
                    'Zaktualizowano wydarzenie w kalendarzu Google:',
                    google_event['id'], google_event['summary'])
        else:
            # Creates a new google event.
            google_event = self.service.events().insert(
                calendarId="primary",
                body=body
            )

            if google_event:
                print(
                    'Utworzono nowe wydarzenie w kalendarzu Google:',
                    google_event['id'], google_event['summary'])

        # Returns event id (created or updated).
        return google_event.get('id')

    def _check_for_update(self, body: dict) -> str | None:
        """
        Checks if a given event already exists in google calendar.
        """
        try:
            # Gets event(s) from google calendar.
            google_events_query = self.service.events().list(
                calendarId='primary',
                timeMin=body['start']['dateTime'],
                timeMax=body['end']['dateTime'],
                q=body['summary'],
                ).execute()

            google_events = google_events_query.get('items', [])

            if len(google_events) > 1:
                raise Exception(
                    'More than one event in google calendar. Should not happen.'
                    )

            for event in google_events:
                print(
                    'znalazłem dopasowanie wydarzenia w kalendarzu Google:',
                    event['id'], event['summary']
                )
                return event['id']

        except Exception as ex:
            print(f'Brak tego wydarzenia w kalendarzu Google. exception: {ex}')
            return None


























# class GoogleCalendarNextEvents(GoogleAuthentication):
#     def get_next_events(self, n=10):
#         """
#         Zwraca n następnych wydarzeń w kalendarzu Google.
#         """

#         try:
#             service = self._get_service()
#             # 'Z' indicates UTC time
#             # now = dt.datetime.utcnow().isoformat() + 'Z'
#             now = dt.datetime.now().isoformat() + 'Z'
#             events_result = (
#                 service.events()
#                 .list(
#                     calendarId='primary',
#                     timeMin=now,
#                     maxResults=n,
#                     singleEvents=True,
#                     orderBy='startTime')
#                 .execute()
#             )

#             # brudna lista z kal google
#             events_g = events_result.get('items', [])

#             # wyczyszczyona lista i odświeżona lista es
#             events = list()

#             for event in events_g:
#                 start = event['start'].get('dateTime', event['start'].get('date'))
#                 description = event['summary']
#                 e = {
#                     'start': start,
#                     'description': description
#                 }
#                 events.append(e)

#         except HttpError as e:
#             logging.exception(f'HttpError {e}')

#         except Exception as e:
#             logging.error(f'Zaskakujący błąd do weryfikacji: {e}')

#         return events
