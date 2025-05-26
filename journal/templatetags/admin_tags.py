from django import template
from journal.models import DescentType, Ritual, DescentSession, Entry
from django.utils import timezone
from django.contrib.auth.models import User

register = template.Library()

@register.inclusion_tag('journal/includes/descent_type_list.html')
def render_descent_type_list():
    descent_types = DescentType.objects.all()
    return {'descent_types': descent_types}

@register.inclusion_tag('journal/includes/ritual_list.html')
def render_ritual_list():
    rituals = Ritual.objects.all()
    return {'rituals': rituals}

@register.inclusion_tag('journal/includes/session_list.html')
def render_session_list():
    sessions = DescentSession.objects.all().order_by('-started_at')
    return {'sessions': sessions}

@register.inclusion_tag('journal/includes/stats.html')
def render_dashboard_stats():
    stats = {
        'total_users': User.objects.count(),
        'total_sessions': DescentSession.objects.count(),
        'active_sessions': DescentSession.objects.filter(completed=False).count(),
        'total_entries': Entry.objects.count(),
        'total_rituals': Ritual.objects.count(),
        'total_descent_types': DescentType.objects.count()
    }
    return {'stats': stats}

@register.inclusion_tag('journal/includes/recent_activity.html')
def render_recent_activity():
    recent_sessions = DescentSession.objects.order_by('-started_at')[:5]
    recent_entries = Entry.objects.order_by('-created_at')[:5]
    return {
        'recent_sessions': recent_sessions,
        'recent_entries': recent_entries
    }