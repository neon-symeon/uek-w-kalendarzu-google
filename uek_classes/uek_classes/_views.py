# views.py

from typing import Any
import json

from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings

from .google_auth import GoogleAuthentication
from .scrap_from_web import ScrapClasses

from googleapiclient.discovery import build

# class Classes(LoginRequiredMixin, TemplateView):
#     template_name = 'classes.html'


class Profile(TemplateView):
    template_name = 'profile.html'


# class ConfirmClasses(TemplateView):
#     """
#     Klasa odpowiedzialna pobranie danych ze strony z wykładami i przekazanie
#     ich do kalendarza Google.
#     """
#     # nazwa template robocza
#     template_name = 'confirm_classes.html'

#     def post(self, request, *args, **kwargs):
#         context = self.get_context_data(**kwargs)

#         request.session['URLS'] = context['urls']

#         return self.render_to_response(context=context)

#     def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
#         context = super().get_context_data(**kwargs)

#         _urls = self.request.POST.getlist('urls[]')
#         self.classes, duplicated = ScrapClasses(urls=_urls).get_classes()

#         context['urls'] = _urls
#         context['classes'] = self.classes
#         context['duplicated'] = duplicated

#         return context


# class AddToGoogleCalendar(TemplateView):
#     template_name = 'add_to_google_calendar.html'

#     def post(self, request, *args, **kwargs):
#         # Pobranie wybranych zajęć bez potrzeby dodatkowego json.loads
#         selected_events = request.POST.getlist("selected_events")

#         # Konfiguracja Google Calendar API
#         service = GoogleAuthentication().get_service()
#         added_event_ids = []

#         for event in selected_events:
#             body = {
#                 'summary': event['summary'],
#                 'start': {
#                     'dateTime': event['start'],
#                     'timeZone': settings.TIME_ZONE
#                 },
#                 'end': {
#                     'dateTime': event['end'],
#                     'timeZone': settings.TIME_ZONE
#                 },
#                 'location': event.get('location', ''),
#                 'description': event.get('description', ''),
#                 'reminders': {
#                     'useDefault': False,
#                 },
#             }

#             google_event = (
#                 service.events()
#                 .insert(calendarId='primary', body=body)
#                 .execute()
#             )
#             added_event_ids.append(google_event.get('id'))

#         # Przekazanie potwierdzenia do szablonu
#         context = self.get_context_data(**kwargs)
#         context['added_event_ids'] = added_event_ids
#         context['selected_events'] = selected_events

#         return self.render_to_response(context=context)


    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     # powinna być lista zdarzeń do wczytania z poprzedniego pliku
    #     # a robię po prostu to co już było, czyli

    #     context['classes'] = self.classes

    #     return context

    # def post(self, request, *args, **kwargs):
    #     context = self.get_context_data(**kwargs)

    #     # Pobranie i wczytanie listy indeksów zaznaczonych wierszy
    #     selected_indices_json = request.POST.get("selected_indices", "[]")
    #     selected_indices = json.loads(selected_indices_json)  # Deserializacja JSON do listy Python

    #     # Dodanie wybranych indeksów do kontekstu
    #     context['classes'] = request.POST.get("classes", "[]")
    #     context['selected_indices'] = selected_indices

    #     return self.render_to_response(context=context)


# class FillTheCalendar(GoogleAuthentication, TemplateView):
#     # nazwa tempalte robocza
#     template_name = 'tokens/google_authentication.html'

#     def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
#         """
#         Przekazuje wszystko co potrzebne do pięknego wyrenderowania info o
#         wykładach i ćwiczeniach przed wysłaniem do kalendarza google.
#         """
#         context = super().get_context_data(**kwargs)

#         return context
