from django.contrib import admin
from .models import DescentType, DescentSession, Entry, Ritual

# Register your models here.
@admin.register(DescentType)
class DescentTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at', 'updated_at')
    search_fields = ('name', 'description')
    ordering = ('-created_at',)

@admin.register(DescentSession)
class DescentSessionAdmin(admin.ModelAdmin):
    list_display = ('user', 'descent_type', 'started_at', 'completed', 'completed_at')
    list_filter = ('descent_type', 'completed')
    search_fields = ('user__username',)
    ordering = ('-started_at',)

@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    list_display = ('session', 'created_at')
    list_filter = ('session__descent_type',)
    search_fields = ('session__user__username', 'prompt')
    ordering = ('-created_at',)

@admin.register(Ritual)
class RitualAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'description', 'created_at')
    list_filter = ('type',)
    search_fields = ('name', 'description')
    ordering = ('-created_at')
