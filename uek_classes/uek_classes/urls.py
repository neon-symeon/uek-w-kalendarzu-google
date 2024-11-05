# urls.py

from django.contrib import admin
from django.urls import path, include


urlpatterns = [

    path('accounts/', include('allauth.urls')),  # allauth's
    path('admin/', admin.site.urls),  # django's
    path("__reload__/", include("django_browser_reload.urls")),  # tailwind's
    # My app(s)
    path("", include("uek_on_google.urls"), name="uek_on_google"),
]
