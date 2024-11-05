from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .simons.scrap_from_web import ScrapClasses
from .simons.google_auth import GoogleCalendarClient


class Links(LoginRequiredMixin, TemplateView):
    """
    Very first screen with links for classes' scrapping.
    """
    template_name = 'uek_on_google/links.html'


class Classes(TemplateView):
    """
    List of classes scrapped from web links given in previous screen.
    """
    template_name = 'uek_on_google/classes.html'

    def _add_to_google_calendar(self, classes):
        """
        Dodaje wybrane wykłady i ćwiczenia do kalendarza Google.
        """
        for c in classes:
            event = GoogleCalendarClient(user_id=self.request.user.pk)
            id = event.create_or_update_event(event=c)
            if id:
                c['id'] = id

        return classes

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Pobiera listę URL z formularza
        _urls = self.request.POST.getlist("urls[]")

        # Ogarnia wykłady i ćwiczenia do potwierdzenia przed
        # dodaniem do kalendarza Google
        classes, duplicated_count = ScrapClasses(urls=_urls).get_classes()

        # Dodaje wybrane wykłady i ćwiczenia do kalendarza Google
        classes = self._add_to_google_calendar(classes)

        # Przekazuje dane do szablonu
        context['urls'] = _urls
        context['classes'] = classes
        context['duplicated_count'] = duplicated_count

        return context

    def post(self, request, *args, **kwargs):
        # Pobiera pieknie przygotowany kontekst do przekazania do szablonu
        context = self.get_context_data(**kwargs)

        # # Przekazuje kontekst do szablonu
        # context['classes'] = context['classes']

        return self.render_to_response(context=context)
