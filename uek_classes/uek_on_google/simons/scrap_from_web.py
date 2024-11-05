
import datetime as dt
import pytz

from bs4 import BeautifulSoup
import requests


class ScrapClasses:
    """
    Class approach for scrapping classes from UEK website.
    """
    def __init__(self, urls: list[str] = None) -> None:
        self._urls = urls

    @property
    def urls(self):
        return self._urls

    @urls.setter
    def urls(self, urls_val):
        """
        Cleaning data - usuwa duplikaty i puste linki.
        """
        # odpuszcza przy braku danych
        if not urls_val:
            return list()
        # usuwa ewentualne duplikaty adresów url
        urls_val = set(urls_val)
        # usuwa ewentualne puste linki
        urls_val = [url for url in urls_val if url]

        self._urls = urls_val

    def get_classes(self) -> tuple[list[dict], int]:
        """
        Znajduje zaplanowane wykłady i ćwiczenia oraz zwraca je w postaci pythonic events.
        Dodatkowo informuje o liczbie usuniętych zajęć w wyniku duplikacji zajęć z języka.
        """
        classes = list()
        for url in self.urls:
            classes.extend(self._extract_classes(url))

        # sortuje wiersze wg daty rozpoczęcia zajęć
        classes.sort(key=lambda x: x['start'])

        # usuwa duplikaty - lektorat to język konkretny jest, dlatego pojawia sie dwa razy
        # dlatego trzeba ten bardziej ogólny wpis usunąć
        i = 0
        duplicated_count = 0
        while i < len(classes) - 1:
            # jeśli datay początku i końca są sobie równe
            if classes[i]['start'] == classes[i + 1]['start']:
                if classes[i]['end'] == classes[i + 1]['end']:
                    # jeśli nazwa zajęć zawiera 'grupa' i nie ma sali zajęć
                    if ('grupa' in classes[i]['summary'].lower()
                        and not classes[i]['location']):
                        # usuwa zdublowany, bardziej ogólny wiersz
                        classes.pop(i)
                        duplicated_count += 1
                    elif ('grupa' in classes[i + 1]['summary'].lower()
                          and not classes[i+1]['location']):
                        # analogicznie
                        classes.pop(i + 1)
            else:
                i += 1

        # uzupełnia wiersz porządkujący zajęcia
        for i in range(len(classes)):
            classes[i]['id'] = i + 1

        return classes, duplicated_count

    def _extract_classes(self, url: str) -> list[dict]:
        """
        Znajduje zaplanowane wykłady i ćwiczenia i zwraca je w postaci
        deserialized, pythonic events.
        """
        # Znajduje wszystkie wiersze tabeli zajęć; pomija pierwszy, z nagłówkami
        table_rows = self.__convert_url_to_soup(url).find_all('tr')[1:]

        classes_from_url = list()

        for row in table_rows:
            cells = row.find_all('td')
            if not cells:
                continue

            date_text = cells[0].text.strip()  # Data zajęć (np. "2024-10-19")
            day_time_text = cells[1].text.strip()  # Dzień tygodnia i godz. zajęć
            subject = cells[2].text.strip()  # Przedmiot
            class_type = cells[3].text.strip()  # Typ zajęć (np. "wykład")
            teacher = cells[4].text.strip()  # Nauczyciel
            room = cells[5].text.strip()  # Sala

            # Dodaje link dla wydarzeń zdalnych.
            link_tag = cells[5].find('a')
            if link_tag:
                href = link_tag.get('href')
                teacher += f'| link do wydarzenia: {href}'

            # Przetwarzanie danych o godzinach zajęć z użyciem funkcji pomocniczej
            beg_datetime, end_datetime = self.__parse_time_range(
                date_text, day_time_text
            )

            # Tworzy obiekt pojedynczych zajęć
            event = {
                'id': '',
                'start': beg_datetime,
                'end': end_datetime,
                'summary': subject + ' | ' + class_type,
                'description': teacher,
                'location': room
            }

            classes_from_url.append(event)

        return classes_from_url

    def __convert_url_to_soup(self, url) -> BeautifulSoup:
        """
        Funkcja pomocnicza.
        Zwraca obiekt jako surowe źródło wszystkich danych ze strony.
        """
        # Pobiera zawartość strony i stwórz obiekt soup
        response = requests.get(url)
        # Ustawia kodowanie na 'utf-8' dla polskich znaków
        response.encoding = 'utf-8'
        # Ogarnia zupę
        soup_per_se = BeautifulSoup(response.text, 'html.parser')

        return soup_per_se

    @staticmethod
    def __parse_time_range(day_str: str, time_str: str) -> tuple[dt.datetime, dt.datetime]:
        """
        Funkcja pomocnicza.
        Parsuje godziny zajęć.
        """
        parts = time_str.split(' ')
        beg_time = parts[1]
        end_time = parts[3]

        # Używa datetime do poprawnego przetworzenia daty i czasu
        date = dt.datetime.strptime(day_str, "%Y-%m-%d")
        beg_hour = dt.datetime.strptime(beg_time, "%H:%M").time()
        end_hour = dt.datetime.strptime(end_time, "%H:%M").time()

        # Uwzględnia strefę czasową-wymóg google calendar
        timezone = pytz.timezone('Europe/Warsaw')
        beg_datetime = timezone.localize(dt.datetime.combine(date, beg_hour))
        end_datetime = timezone.localize(dt.datetime.combine(date, end_hour))

        return beg_datetime, end_datetime
