from django.contrib import admin
from .models import ItineraryGenerator

class ItineraryGeneratorAdmin(admin.ModelAdmin):
    list_display = ('user', 'destination', 'api_response')
    search_fields = ('user__username', 'destination')

admin.site.register(ItineraryGenerator, ItineraryGeneratorAdmin)

