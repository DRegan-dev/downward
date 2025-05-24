from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import DescentType, DescentSession, Entry, Ritual

# Create your views here.
def home(request):
    """
        Homepage view for Downward
        Acessible to all users
    """

    return render(request, 'journal/home.html')

def about(request):
    """
    About page explaining the purpose of Downward
    """
    context = {
        'sections': [
            {
                'title': 'Our Purpose',
                'content': 'Downward is a private, guided space for exploring mental, emotional, and existential journeys. Unlike traditional journaling tools, we embrace the neccessary descent - moments when we step back, slow down, or let go.'
            },
            {
                'title': 'Why Descent?',
                'content': 'We believe that not every fail is a failure. Somtimes, going own is the only way to truly understand ourselves. Our platform provides a safe, structured environment for processing decline, loss, burnout, and complexity.'
            },
            {
                'title': 'How It Works',
                'content': 'Through guided sessions, reflective prompts, and optional rituals, Downward helps you exploreyour descent in a meaningful way. Our structured approach ensures you can process your journey while maintaining privacy and control.'
            }
        ], 
        'values': [
            'Emotional Authenticity',
            'Guided Reflection',
            'Non-judgemental Processing',
            'Structured Exploration',
            'Privacy First'
        ]
    }
    return render(request, 'journal/about.html', context)

def privacy(request):
    """
    Privacy policy page
    """
    context = {
        'sections': [
            {
                'title': 'Data Collection',
                'content': 'We collect only the minimum data neccesary for your descent sessions. This includesyour username, email address, and session data. No personal data is shared with third parties.'
            },
            {
                'title': 'Session Data',
                'content': 'Your descent session data is stored securely and is accessible only to you. We do not analyze or use your session content for any purposes other than providing the service.'
            },
            {
                'title': 'Security Measures',
                'content': 'All data is encrypted both at rest and in transit. We implement industry standard security practicesto protect your information.'
            },
            {
                'title': 'Your Rights',
                'content': 'You have the right to view, modify, or delete your session data at any time. You can laso request a complete data export.'
            }
        ]
    }
    return render(request, 'journal/privacy.html', context)

def terms(request):
    """
    Terms of Service page
    """
    context = {
        'sections': [
            {
                'title': 'Acceptance of Terms',
                'content': 'By using Downward, you agree to ther Terms of Service and our Privacy Policy. Please read them carefully before using our service.'
            },
            {
                'title': 'User Conduct',
                'content': 'You agree to use Downward in a respectful and appropriate manner. The Platform is intended for personal reflection and emotional processing.'
            },
            {
                'title': 'Intellectual Property',
                'content': 'All content you create through Downward remains your property. However, you grant us a license to store and display this content as necessary for the operation of the service.'
            },
            {
                'title': 'Termination',
                'content': 'We reserve the right to terminate or suspend your account if you violate these Terms of Service. You can also delete your account at any time.'
            }
        ]
    }
    return render(request, 'journal/terms.html', context)

@login_required
def admin_dashboard(request):
    """
    Custom admin dashboard with statistic and quick actions
    """
    if not request.user.is_superuser:
        messages.error(request, "You don't have permission to access this page.")
        return redirect('home')
    
    context = {
        'total_users': User.objects.count(),
        'total_sessions': DescentSession.objects.count(),
        'active_sessions': DescentSession.objects.filter(completed=False).count(),
        'total_entries': Entry.objects.count(),
        'recent_sessions': DescentSession.objects.order_by('-started_at')[:5],
        'recent_entries': Entry.objects.order_by('-created_at')[:5],
        'rituals': Ritual.objects.all()
    }
    return render(request, 'journal/admin_dashboard.html', context)