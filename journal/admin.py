from django.contrib import admin
from .models import DescentType, DescentSession, Entry, Ritual

# Register your models here.
@admin.register(DescentType)
class DescentTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at')
    list_filter = ('type', 'created_at')
    search_fields = ('name', 'description')
    

@admin.register(DescentSession)
class DescentSessionAdmin(admin.ModelAdmin):
    list_display = ('user', 'descent_type','status', 'started_at', 'duration')
    list_filter = ('status', 'descent_type', 'started_at')
    search_fields = ('user__username', 'descent_type__name', 'notes')
    readonly_fields = ('duration',)

    def duration(self, obj):
        return obj.duration
    duration.short_description = 'Duration'

@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    list_display = ('session', 'timestamp', 'emotion_level')
    list_filter = ('emotion_level', 'timestamp')
    search_fields = ('content', 'reflection')
    ordering = ('-timestamp',)

@admin.register(Ritual)
class RitualAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'created_at')
    list_filter = ('type', 'created_at')
    search_fields = ('name', 'description', 'instructions')
