from django.contrib import admin
from .models import DescentType, DescentSession, Entry

# Register your models here.
@admin.register(DescentType)
class DescentTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at')
    # list_filter = ('type', 'created_at')
    search_fields = ('name', 'description')
    ordering = ('name',)
    fieldsets = (
        (None, {
            'fields': ('name', 'type', 'description')
        }),
        ('Metadata', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        })
    )
    readonly_fields = ('created_at',)
    

@admin.register(DescentSession)
class DescentSessionAdmin(admin.ModelAdmin):
    list_display = ('user', 'descent_type','status', 'started_at', 'duration')
    list_filter = ('status', 'descent_type', 'started_at')
    search_fields = ('user__username', 'notes')
    ordering = ('-started_at',)
    fieldsets = (
        (None, {
            'fields': ('User', 'descent_type', 'status', 'notes')
        }),
        ('Timestamps', {
            'fields': ('started_at', 'completed_at', 'abandoned_at'),
            'classes': ('collapse',)
        })
    )
    readonly_fields = ('started_at', 'completed_at', 'abandoned_at')

    def duration(self, obj):
        return obj.duration
    duration.short_description = 'Duration'

    def duration(self, obj):
        """Calculate the duration of the descent session"""
        if obj.completed_at:
            return obj.completed_at - obj.started_at
        elif obj.abandoned_at:
            return obj.abandoned_at - obj.started_at
        return timezone.timedelta()
    duration.short_description = 'Duration'

@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    list_display = ('session', 'timestamp', 'emotion_level')
    list_filter = ('emotion_level', 'timestamp')
    search_fields = ('content', 'reflection')
    ordering = ('-timestamp',)
    fieldsets = (
        (None, {
            'fields': ('session', 'content', 'reflection', 'emotion_level')
        }),
        ('Metadata', {
            'fields': ('timestamp',),
            'classes': ('collapse',)
        })
    )
    readonly_fields = ('timestamp',)


