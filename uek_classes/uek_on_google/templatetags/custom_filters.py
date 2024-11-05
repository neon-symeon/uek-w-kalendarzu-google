"""
filtry dodane dla przejrzystości kodu.
"""
# tokens/templatetags/custom_filters.py

from django import template

register = template.Library()


@register.filter
def date_n_time(value):
    """
    Zwraca datę i godzinę w formacie: '19.09.24 g.10:23'.
    """
    if value:
        return value.astimezone().strftime('%d.%m.%y g.%H:%M')
    return ''

@register.filter
def time_only(value):
    """
    Zwraca datę i godzinę w formacie: '10:23'.
    """
    if value:
        return value.astimezone().strftime('%H:%M')
    return ''
