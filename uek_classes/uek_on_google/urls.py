from django.urls import path
from . import views

app_name = 'uek_on_google'

urlpatterns = [
    path('', views.Links.as_view(), name='links'),
    path('classes/', views.Classes.as_view(), name='classes'),
]
