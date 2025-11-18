from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm, UserChangeForm
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import DescentTypeForm, DescentSessionForm, EntryForm
from .models import DescentSession, DescentType, Entry


def home(request):
    """Homepage view for Downward. Accessible to all users."""
    return render(request, 'journal/home.html')


def about(request):
    """About page explaining the purpose of Downward."""
    context = {
        'sections': [
            {
                'title': 'Our Purpose',
                'content': (
                    'Downward is a private, guided space for exploring '
                    'mental, emotional, and existential journeys. Unlike '
                    'traditional journaling tools, we embrace the necessary '
                    'descent - moments when we step back, slow down, or '
                    'let go.'
                ),
            },
            {
                'title': 'Why Descent?',
                'content': (
                    'We believe that not every fail is a failure. Sometimes, '
                    'going down is the only way to truly understand ourselves. '
                    'Our platform provides a safe, structured environment for '
                    'processing decline, loss, burnout, and complexity.'
                ),
            },
            {
                'title': 'How It Works',
                'content': (
                    'Through guided sessions, reflective prompts, and '
                    'optional rituals, Downward helps you explore your '
                    'descent in a meaningful way. Our structured approach '
                    'ensures you can process your journey while maintaining '
                    'privacy and control.'
                ),
            },
        ],
        'values': [
            'Emotional Authenticity',
            'Guided Reflection',
            'Non-judgemental Processing',
            'Structured Exploration',
            'Privacy First',
        ],
    }
    return render(request, 'journal/about.html', context)


def privacy(request):
    """Privacy policy page."""
    context = {
        'sections': [
            {
                'title': 'Data Collection',
                'content': (
                    'We collect only the minimum data necessary for your '
                    'descent sessions. This includes your username, email '
                    'address, and session data. No personal data is shared '
                    'with third parties.'
                ),
            },
            {
                'title': 'Session Data',
                'content': (
                    'Your descent session data is stored securely and is '
                    'accessible only to you. We do not analyze or use your '
                    'session content for any purposes other than providing '
                    'the service.'
                ),
            },
            {
                'title': 'Security Measures',
                'content': (
                    'All data is encrypted both at rest and in transit. We '
                    'implement industry standard security practices to '
                    'protect your information.'
                ),
            },
            {
                'title': 'Your Rights',
                'content': (
                    'You have the right to view, modify, or delete your '
                    'session data at any time. You can also request a '
                    'complete data export.'
                ),
            },
        ]
    }
    return render(request, 'journal/privacy.html', context)


def terms(request):
    """Terms of Service page."""
    context = {
        'sections': [
            {
                'title': 'Acceptance of Terms',
                'content': (
                    'By using Downward, you agree to these Terms of Service '
                    'and our Privacy Policy. Please read them carefully before '
                    'using our service.'
                ),
            },
            {
                'title': 'User Conduct',
                'content': (
                    'You agree to use Downward in a respectful and appropriate '
                    'manner. The Platform is intended for personal reflection '
                    'and emotional processing.'
                ),
            },
            {
                'title': 'Intellectual Property',
                'content': (
                    'All content you create through Downward remains your '
                    'property. However, you grant us a license to store and '
                    'display this content as necessary for the operation of '
                    'the service.'
                ),
            },
            {
                'title': 'Termination',
                'content': (
                    'We reserve the right to terminate or suspend your '
                    'account if you violate these Terms of Service. You can '
                    'also delete your account at any time.'
                ),
            },
        ]
    }
    return render(request, 'journal/terms.html', context)


@login_required
def admin_dashboard(request):
    """Custom admin dashboard with statistics and quick actions."""
    context = {
        'total_users': User.objects.count(),
        'total_sessions': DescentSession.objects.count(),
        'active_sessions': DescentSession.objects.filter(
            status__in=['STARTED', 'IN_PROGRESS']
        ).count(),
        'total_entries': Entry.objects.count(),
        'total_descent_types': DescentType.objects.count(),
    }
    return render(request, 'journal/admin_dashboard.html', context)


@login_required
def start_descent(request):
    """Start a new descent session."""
    if request.method == 'POST':
        form = DescentSessionForm(request.POST, user=request.user)
        if form.is_valid():
            session = form.save(commit=False)
            session.user = request.user
            session.status = 'Started'
            session.save()
            messages.success(request, 
                            'Descent session started successfully!'
            )
            return redirect('journal:continue_descent', pk=session.pk)
        messages.error(request, 'Please correct the errors below.')
    else:
        form = DescentSessionForm(user=request.user)
        form.fields['descent_type'].queryset = DescentType.objects.filter(
            is_active=True
        )

    return render(request, 'journal/start_descent.html', {'form': form})


@login_required
def descent_start(request, pk):
    session = get_object_or_404(DescentSession, pk=pk)
    if session.user != request.user:
        messages.error(
            request, "You don't have permission to access this session."
        )
        return redirect('journal_history')

    return render(request, 'journal/descent_start.html', {'session': session})


@login_required
def continue_descent(request, pk):
    session = get_object_or_404(DescentSession, pk=pk, user=request.user)
    entries = Entry.objects.filter(session=session).order_by('timestamp')

    if request.method == 'POST':
        content = request.POST.get('content')
        emotion_level = request.POST.get('emotion_level')
        reflection = request.POST.get('reflection')
        action = request.POST.get('action')

        if not content or not emotion_level:
            messages.error(request, 'Content and emotion level are required.')
            return redirect('journal:continue_descent', pk=pk)

        try:
            emotion_level = int(emotion_level)
            if emotion_level < 1 or emotion_level > 5:
                raise ValueError('Invalid emotion level')

            Entry.objects.create(
                session=session,
                content=content,
                emotion_level=emotion_level,
                reflection=reflection,
            )

            if action == 'complete':
                session.status = 'COMPLETED'
                session.completed_at = timezone.now()
                session.save()
                messages.success(request, 'Session completed successfully!')
                return redirect('journal:complete_descent', pk=pk)

            if action == 'save_progress':
                if session.status != 'IN_PROGRESS':
                    session.status = 'IN_PROGRESS'
                    session.save()
                messages.success(
                    request,
                    'Entry added successfully. Continue your descent.',
                )
                return redirect('journal:journal_history')

            messages.success(request, 'Entry added successfully.')
            return redirect('journal:complete_descent', pk=pk)

        except (ValueError, TypeError):
            messages.error(
                request,
                'Invalid emotion level. Please select a number between 1 and 5.',
            )
            return redirect('journal:continue_descent', pk=pk)

    return render(
        request,
        'journal/continue_descent.html',
        {'session': session, 'entries': entries},
    )


@login_required
def edit_session(request, pk):
    session = get_object_or_404(DescentSession, pk=pk, user=request.user)
    entries = Entry.objects.filter(session=session).order_by('timestamp')

    if request.method == 'POST':
        if 'complete_session' in request.POST:
            session.status = 'Completed'
            session.completed_at = timezone.now()
            session.save()
            messages.success(
                request, 'Session marked as completed successfully'
            )
            return redirect('journal:journal_history')

        for entry in entries:
            content_key = f'content_{entry.id}'
            emotion_key = f'emotion_level_{entry.id}'
            reflection_key = f'reflection_{entry.id}'

            if content_key in request.POST:
                entry.content = request.POST[content_key]
                entry.emotion_level = request.POST[emotion_key]
                entry.reflection = request.POST[reflection_key]
                entry.save()

        messages.success(request, 'Session updated successfully!')
        return redirect('journal:session_detail', pk=pk)

    return render(
        request,
        'journal/edit_session.html',
        {'session': session, 'entries': entries},
    )


@login_required
def complete_descent(request, pk):
    session = get_object_or_404(DescentSession, pk=pk, user=request.user)
    session.status = 'COMPLETED'
    session.completed_at = timezone.now()
    session.save()
    messages.success(request, 'Session marked as completed successfully!')
    return redirect('journal:journal_history')


@login_required
def abandon_descent(request, pk):
    session = get_object_or_404(DescentSession, pk=pk, user=request.user)
    session.status = 'ABANDONED'
    session.completed_at = timezone.now()
    session.save()
    return redirect('journal:home')


@login_required
@require_POST
def add_entry(request, pk):
    session = get_object_or_404(DescentSession, pk=pk, user=request.user)

    if request.method == 'POST':
        form = EntryForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.session = session
            entry.save()
            messages.success(request, 'Entry added successfully!')
            return redirect('journal:continue_descent', pk=session.pk)
        messages.error(request, 'Please correct the errors below.')

    form = EntryForm()
    context = {'form': form, 'session': session}
    return render(request, 'journal/add_entry.html', context)


@login_required
def edit_entry(request, entry_id):
    entry = get_object_or_404(Entry, id=entry_id, session__user=request.user)

    if request.method == 'POST':
        form = EntryForm(request.POST, instance=entry)
        if form.is_valid():
            form.save()
            messages.success(request, 'Entry updated successfully!')
            return redirect('journal:continue_descent', pk=entry.session.pk)
        messages.error(request, 'Please correct the errors below.')

    form = EntryForm(instance=entry)
    context = {'form': form, 'entry': entry, 'emotion_levels': range(1, 6)}
    return render(request, 'journal/edit_entry.html', context)


@login_required
@require_POST
def delete_entry(request, entry_id):
    entry = get_object_or_404(Entry, pk=entry_id, session__user=request.user)
    session_pk = entry.session.pk

    if request.method == 'POST':
        entry.delete()
        messages.success(request, 'Entry deleted successfully.')
        return redirect('journal:continue_descent', pk=session_pk)

    return render(
        request,
        'journal/confirm_delete.html',
        {
            'object': entry,
            'cancel_url': reverse(
                'journal:coninue_descent', kwargs={'pk': session_pk}
            ),
            'object_type': 'entry',
        },
    )


@login_required
def journal_history(request):
    """Display User's descent history."""
    sessions = (
        DescentSession.objects.prefetch_related('entries')
        .filter(user=request.user)
        .order_by('-started_at')
    )
    return render(
        request, 'journal/journal_history.html', {'sessions': sessions}
    )


@login_required
def descent_type_list(request):
    """List all descent types with management options."""
    if not request.user.is_superuser:
        messages.error(
            request, "You don't have permission to access this page."
        )
        return redirect('journal:home')

    descent_types = DescentType.objects.all()
    return render(
        request,
        'journal/includes/descent_type_list.html',
        {'descent_types': descent_types},
    )


@login_required
def descent_type_add(request):
    if not request.user.is_superuser:
        messages.error(
            request, "You don't have permission to add descent types."
        )
        return redirect('journal:home')

    if request.method == 'POST':
        form = DescentTypeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Descent Type added succesfully.')
            return redirect('journal:admin_dashboard')
    else:
        form = DescentTypeForm()

    return render(
        request,
        'journal/includes/form.html',
        {'form': form, 'title': 'Add Descent Type', 'action': 'Add'},
    )


@login_required
def descent_type_edit(request, pk):
    if not request.user.is_superuser:
        messages.error(
            request, "You don't have permission to edit descent types."
        )
        return redirect('journal:home')

    descent_type = get_object_or_404(DescentType, pk=pk)

    if request.method == 'POST':
        form = DescentTypeForm(request.POST, instance=descent_type)
        if form.is_valid():
            form.save()
            messages.success(request, 'Descent Type updated succesfully.')
            return redirect('journal:admin_dashboard')
    else:
        form = DescentTypeForm(instance=descent_type)

    return render(
        request,
        'journal/includes/form.html',
        {'form': form, 'title': 'Edit Descent Type', 'action': 'Update'},
    )


@login_required
def descent_type_delete(request, pk):
    if not request.user.is_superuser:
        messages.error(
            request, "You don't have permission to edit descent types."
        )
        return redirect('journal:home')

    descent_type = get_object_or_404(DescentType, pk=pk)
    descent_type.delete()
    messages.success(request, 'Descent Type deleted successfully')
    return redirect('journal:admin_dashboard')


@login_required
def session_list(request):
    if not request.user.is_superuser:
        return redirect('home')

    sessions = DescentSession.objects.all().order_by('-started_at')
    return render(request, 'journal/session_list.html', {'sessions': sessions})


@login_required
def session_detail(request, pk):
    session = get_object_or_404(DescentSession, pk=pk, user=request.user)

    if request.method == 'POST' and 'complete_session' in request.POST:
        if session.status != 'COMPLETED':
            session.status = 'COMPLETED'
            session.completed_at = timezone.now()
            session.save()
            messages.success(
                request, 'Session marked as completed successfully!'
            )
            return redirect('journal:journal_history')
        messages.warning(request, 'This session is already completed.')
        return redirect('journal:journal_history')

    entries = Entry.objects.filter(session=session).order_by('timestamp')
    context = {'session': session, 'entries': entries}
    return render(request, 'journal/session_detail.html', context)


@login_required
def session_edit(request, pk):
    """Edit a descent session."""
    if not request.user.is_superuser:
        messages.error(
            request, "You don't have permission to edit sessions."
        )
        return redirect('home')

    session = get_object_or_404(DescentSession, pk=pk)

    if request.method == 'POST':
        form = DescentSessionForm(request.POST, instance=session)
        if form.is_valid():
            form.save()
            messages.success(request, 'Session updated successfully.')
            return redirect('session_list')
    else:
        form = DescentSessionForm(instance=session)

    context = {'form': form, 'session': session}
    return render(request, 'journal/session_edit.html', context)


@login_required
def session_delete(request, pk):
    session = get_object_or_404(DescentSession, pk=pk, user=request.user)

    if request.method == 'POST':
        session.delete()
        messages.success(request, 'Session deleted successfully.')
        return redirect('journal:journal_history')

    context = {'session': session}
    return render(request, 'journal/session_confirm_delete.html', context)


@login_required
def user_list(request):
    if not request.user.is_superuser:
        messages.error(request, "You don't have permission to edit sessions.")
        return redirect('home')

    users = User.objects.all()
    return render(request, 'journal/user_list.html', {'users': users})


@login_required
def user_edit(request, pk):
    if not request.user.is_superuser:
        messages.error(request, "You don't have permission to edit users.")
        return redirect('home')

    user = get_object_or_404(User, pk=pk)

    if request.method == 'POST':
        user_form = UserChangeForm(request.POST, instance=user)
        password_form = PasswordChangeForm(user, request.POST)

        if user_form.is_valid():
            user_form.save()
            messages.success(
                request, 'User information updated successfully.'
            )

            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Password updated Successfully.')

            return redirect('user_list')
    else:
        user_form = UserChangeForm(instance=user)
        password_form = PasswordChangeForm(user)

    return render(
        request,
        'journal/user_edit.html',
        {'user_form': user_form, 'password_form': password_form, 'user': user},
    )


@login_required
def user_delete(request, pk):
    if not request.user.is_superuser:
        messages.error(request, "You don't have permission to delete users.")
        return redirect('home')

    user = get_object_or_404(User, pk=pk)

    if User.objects.filter(is_superuser=True).count() == 1 and user.is_superuser:
        messages.error(request, 'Cannot delete the last superuser')
        return redirect('user_list')

    user.delete()
    messages.success(request, 'User deleted successfully.')
    return redirect('user_list')
