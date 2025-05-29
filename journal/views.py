from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count
from django.utils import timezone
from .models import DescentType, DescentSession, Entry, Ritual
from .forms import DescentTypeForm, RitualForm
from django.contrib.auth.models import User
import datetime

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
                'content': 'Downward is a private, guided space for exploring mental, emotional, and existential journeys. Unlike traditional journaling tools, we embrace the necessary descent - moments when we step back, slow down, or let go.'
            },
            {
                'title': 'Why Descent?',
                'content': 'We believe that not every fail is a failure. Sometimes, going down is the only way to truly understand ourselves. Our platform provides a safe, structured environment for processing decline, loss, burnout, and complexity.'
            },
            {
                'title': 'How It Works',
                'content': 'Through guided sessions, reflective prompts, and optional rituals, Downward helps you explore your descent in a meaningful way. Our structured approach ensures you can process your journey while maintaining privacy and control.'
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
                'content': 'We collect only the minimum data necesary for your descent sessions. This includes your username, email address, and session data. No personal data is shared with third parties.'
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
                'content': 'You have the right to view, modify, or delete your session data at any time. You can also request a complete data export.'
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
                'content': 'By using Downward, you agree to these Terms of Service and our Privacy Policy. Please read them carefully before using our service.'
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
    
    # Get statistics
    context = {
        'total_users': User.objects.count(),
        'total_sessions': DescentSession.objects.count(),
        'active_sessions': DescentSession.objects.filter(status__in=['STARTED', 'IN_PROGRESS']).count(),
        'total_entries': Entry.objects.count(),
        'total_rituals': Ritual.objects.count(),
        'total_descent_types': DescentType.objects.count()
    }
    
    return render(request, 'journal/admin_dashboard.html', context)

@login_required
def start_descent(request):
    """
    Start a new descent session
    """

    if request.method == 'POST':
        # Get selected descent type
        descent_type_id = request.POST.get('descent_type')
        descent_type = get_object_or_404(DescentType, pk=descent_type_id)

        # Create new descent session
        session = DescentSession.objects.create(
            user=request.user,
            descent_type=descent_type,
            status='STARTED'
        )
        return redirect('journal:continue_descent', pk=session.pk)
    
    descent_types = DescentType.objects.all()
    return render(request, 'journal/start_descent.html', {
        'descent_types': descent_types
    })



@login_required
def descent_start(request, pk):
    session = get_object_or_404(DescentSession, pk=pk)

    if session.user != request.user:
        messages.error(request, "You don't have permission to access this session.")
        return redirect('journal_history')
    
    # Get during-descent rituals
    during_rituals = Ritual.objects.filter(type='DURING')

    return render(request, 'journal/descent_start.html', {
        'session': session,
        'during_rituals': during_rituals
    })

@login_required
def continue_descent(request, pk):
    session = get_object_or_404(DescentSession, pk=pk, user=request.user)

    if request.method == 'POST':
        content = request.POST.get('content')
        emotion_level = request.POST.get('emotion-level')
        reflection = request.POST.get('reflection')

        if not content or not emotion_level:
            messages.error(request, "Content and emotion level are required.")
            return redirect('journal:continue_descent', pk=pk)
        
        try:
            emotion_level = int(emotion_level)
            if emotion_level < 1 or emotion_level > 5:
                raise ValueError('Invalid emotion level')

            Entry.objects.create(
                session=session,
                content=content,
                emotion_level=emotion_level,
                reflection=reflection
            )

            messages.success(request, "Entry added successfully.")
            return redirect('journal:continue_descent', pk=pk)

        except (ValueError, TypeError) as e:
            messages.error(request, 'Invalid emotion level. Please select a number between 1 and 5.')
            return redirect('journal:continue_descent', pk=pk)
  
    pre_rituals = Ritual.objects.filter(descent_type=session.descent_type, type='PRE')
    during_rituals = Ritual.objects.filter(descent_type=session.descent_type, type='DURING')
    
    return render(request, 'journal/continue_descent.html', {
        'session': session,
        'pre_rituals': pre_rituals,
        'during_rituals': during_rituals
    })

@login_required
def complete_descent(request, pk):
    session = get_object_or_404(DescentSession, pk=pk, user = request.user)    
    session.status = 'COMPLETED'
    session.completed_at = timezone.now()
    session.save()
    return redirect('journal:home')

@login_required
def abandon_descent(request, pk):
    session = get_object_or_404(DescentSession, pk=pk, user=request.user)    
    session.status = 'ABANDONED'
    session.completed_at = timezone.now()
    session.save()
    return redirect('journal:home')

@login_required
def journal_history(request):
    """
    Display User's descent history
    """
    # Get all sessions for the current user
    sessions = DescentSession.objects.filter(user=request.user).order_by('-started_at')

    context = {
        'sessions': sessions,
        'descent_types': DescentType.objects.all()
    }
    return render(request, 'journal/journal_history.html', context)

# Descent Type Views
@login_required
def descent_type_list(request):
    """
    List all descent types with management options
    """
    if not request.user.is_superuser:
        messages.error(request, "You don't have permission to access this page.")
        return redirect('journal:home')
    
    descent_types = DescentType.objects.all()
    return render(request, 'journal/descent_type_list.html', {
        'descent_types': descent_types
    })

@login_required
def descent_type_add(request):
    if not request.user.is_superuser:
        messages.error(request, "You don't have permission to add descent types.")
        return redirect('journal:home')
    
    if request.method == "POST":
        form = DescentTypeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Descent Type added succesfully.')
            return redirect('journal:descent_type_list')
    else:
        form = DescentTypeForm()

    return render(request, 'journal/includes/form.html', {
        'form':  form,
        'title': 'Add Descent Type',
        'action': 'Add'
    })        
    
@login_required
def descent_type_edit(request, pk):
    if not request.user.is_superuser:
        messages.error(request, "You don't have permission to edit descent types.")
        return redirect('journal:home')
    
    descent_type = get_object_or_404(DescentType, pk=pk)
    
    if request.method == "POST":
        form = DescentTypeForm(request.POST, instance=descent_type)
        if form.is_valid():
            form.save()
            messages.success(request, 'Descent Type updated succesfully.')
            return redirect('journal:descent_type_list')
    else:
        form = DescentTypeForm(instance=descent_type)

    return render(request, 'journal/includes/form.html', {
        'form':  form,
        'title': 'Edit Descent Type',
        'action': 'Update'
    })  

@login_required
def descent_type_delete(request, pk):
    if not request.user.is_superuser:
        messages.error(request, "You don't have permission to edit descent types.")
        return redirect('journal:home')
    
    descent_type = get_object_or_404(DescentType, pk=pk)
    descent_type.delete()
    messages.success(request, 'Descent Type deleted successfully')
    return redirect('journal:descent_type_list')

# Ritual Views
@login_required
def ritual_list(request):
    if not request.user.is_superuser:
        messages.error(request, "You don't have permission to manage rituals.")
        return redirect('journal:home')
    
    rituals = Ritual.objects.all()
    return render(request, 'journal/ritual_list.html', {
        'rituals': rituals
    })

@login_required
def ritual_add(request):
    if not request.user.is_superuser:
        messages.error(request, "You don't have permission to add rituals.")
        return redirect('home')
    
    if request.method == 'POST':
        form = RitualForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ritual added succesfully.')
            return redirect('ritual_list')
    else:
        form = RitualForm()

    return render(request, 'journal/includes/form.html', {
        'form':  form,
        'title': 'Add Ritual',
        'action': 'Add'
    })    
    
@login_required
def ritual_edit(request, pk):
    if not request.user.is_superuser:
        messages.error(request, "You don't have permission to edit rituals.")
        return redirect('home')
    
    ritual = get_object_or_404(Ritual, pk=pk)
    
    if request.method == 'POST':
        form = RitualForm(request.POST, instance=ritual)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ritual updated succesfully.')
            return redirect('ritual_list')
    else:
        form = RitualForm(instance=ritual)

    return render(request, 'journal/includes/form.html', {
        'form':  form,
        'title': 'Edit Ritual',
        'action': 'Update'
    })  

@login_required
def ritual_delete(request, pk):
    if not request.user.is_superuser:
        messages.error(request, "You don't have permission to edit sessions.")
        return redirect('home')
    
    ritual = get_object_or_404(Ritual, pk=pk)
    ritual.delete()
    messages.success(request, 'Ritual deleted succcesfully.')
    return redirect('ritual_list')

# Session Views

@login_required
def session_list(request):
    if not request.user.is_superuser:
        return redirect('home')

    sessions = DescentSession.objects.all().order_by('-started_at')
    return render(request, 'journal/session_list.html', {
        'sessions': sessions
    })

@login_required
def session_detail(request, pk):
    session = get_object_or_404(DescentSession, pk=pk, user=request.user)

    # Get all entries for this session
    entries = Entry.objects.filter(session=session).order_by('timestamp')

    # Get rituals for this session type
    pre_rituals = Ritual.objects.filter(descent_type=session.descent_type, type='PRE')
    during_rituals = Ritual.objects.filter(descent_type=session.descent_type, type='DURING')

    context = {
        'session': session,
        'entries': entries,
        'pre_rituals': pre_rituals,
        'during_rituals': during_rituals
    }

    return render(request, 'journal/session_detail.html', context)



@login_required
def session_edit(request, pk):
    """
    Edit a descent session
    """
    if not request.user.is_superuser:
        messages.error(request, "You don't have permission to edit sessions.")
        return redirect('home')
    
    session = get_object_or_404(DescentSession, pk=pk)
        
    if request.method == 'POST':
        form = SessionForm(request.POST, instance=session)
        if form.is_valid:
            form.save()
            messages.success(request, 'Session updated successfully.')
            return redirect('session_list')
    else:
        form = SessionForm(instance=session)

    context = {
        'form': form,
        'session': session
    }        
    return render(request, 'journal/session_edit.html', context)
    
@login_required
def session_delete(request, pk):
    session = get_object_or_404(DescentSession, pk=pk, user=request.user)

    if request.method == 'POST':       
        session.delete()
        messages.success(request, 'Session deleted successfully.')
        return redirect('journal:journal_history')
    
    return render(request, 'journal/session_confirm_delete.html', {
        'session': session
    })

@login_required
def user_list(request):
    if not request.user.is_superuser:
        messages.error(request, "You don't have permission to edit sessions.")
        return redirect('home')
    
    users = User.objects.all()
    return render(request, 'journal/user_list.html', {
        'users': users
    })

@login_required
def user_edit(request, pk):
    if not request.user.is_superuser:
        messages.error(request, "You don't have permission to edit users.")
        return redirect('home')
    
    user = get_object_or_404(User, pk=pk)

    if request.method == 'POST':
        # update basic user info
        user_form = UserChangeForm(request.POST, instance=user)
        password_form = PasswordChangeForm(user, request.POST)

        if user_form.is_valid():
            user_form.save()
            messages.success(request, 'User information updated successfully.')

            # Update password if provided
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Password updated Successfully.')

            return redirect('user_list')
    else:
        user_form = UserChangeForm(instance=user)
        password_form = PasswordChangeForm(user)
    
    return render(request, 'journal/user_edit.html', {
        'user_form': user_form,
        'password_form': password_form,
        'user': user
    })

@login_required
def user_delete(request, pk):
    if not request.user.is_superuser:
        messages.error(request, "You don't have permission to delete users.")
        return redirect('home')
    
    user = get_object_or_404(User, pk=pk)

    # Prevent deleteion of the last Superuser
    if User.objects.filter(is_superuser=True).count() == 1 and user.is_superuser:
        messages.error(request, 'Cannot delete the last superuser')
        return redirect('user_list')
    
    user.delete()
    messages.success(request, 'User deleted successfully.')
    return redirect('user_list')
