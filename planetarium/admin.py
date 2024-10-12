from django.contrib import admin

from planetarium.models import (
    PlanetariumDome,
    ShowTheme,
    ShowSession,
    AstronomyShow,
    Reservation,
    Ticket,
)


admin.site.register(PlanetariumDome)
admin.site.register(ShowTheme)
admin.site.register(ShowSession)
admin.site.register(AstronomyShow)
admin.site.register(Reservation)
admin.site.register(Ticket)
