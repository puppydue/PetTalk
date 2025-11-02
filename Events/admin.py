from django.contrib import admin
from .models import Event

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'location', 'status', 'creator')
    list_filter = ('status', 'date')
    search_fields = ('title', 'location')
