from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from .forms import SecureLoginForm, SecureUserCreationForm, SecurePasswordChangeForm, UserProfileForm
from .models import CustomUser, LoginAttempt, UserSession


def get_client_ip(request):
    """Get client IP address from request"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def user_login(request):
    """
    Secure login view with attempt tracking and account lockout
    """
    if request.user.is_authenticated:
        return redirect('healthcenter:home')

    if request.method == 'POST':
        form = SecureLoginForm(request, data=request.POST)
        username = request.POST.get('username')
        password = request.POST.get('password')
        remember_me = request.POST.get('remember_me')

        ip_address = get_client_ip(request)
        user_agent = request.META.get('HTTP_USER_AGENT', '')

        try:
            user = CustomUser.objects.get(username=username)

            # Check if account is locked
            if user.is_account_locked():
                LoginAttempt.objects.create(
                    username=username,
                    ip_address=ip_address,
                    user_agent=user_agent,
                    success=False,
                    failure_reason='Account locked'
                )
                messages.error(request, f'Account is locked due to too many failed login attempts. Please try again later.')
                return render(request, 'accounts/login.html', {'form': form})

        except CustomUser.DoesNotExist:
            # Log failed attempt for non-existent user
            LoginAttempt.objects.create(
                username=username,
                ip_address=ip_address,
                user_agent=user_agent,
                success=False,
                failure_reason='User does not exist'
            )

        if form.is_valid():
            user = form.get_user()

            # Reset failed login attempts
            user.reset_failed_login()

            # Update last login IP
            user.last_login_ip = ip_address
            user.save(update_fields=['last_login_ip'])

            # Log successful login
            LoginAttempt.objects.create(
                username=username,
                ip_address=ip_address,
                user_agent=user_agent,
                success=True
            )

            # Set session expiry
            if not remember_me:
                request.session.set_expiry(0)  # Session expires when browser closes
            else:
                request.session.set_expiry(1209600)  # 2 weeks

            login(request, user)

            # Create session tracking after login (when session_key is guaranteed to exist)
            # Use update_or_create to avoid duplicate session_key errors
            if request.session.session_key:
                UserSession.objects.update_or_create(
                    session_key=request.session.session_key,
                    defaults={
                        'user': user,
                        'ip_address': ip_address,
                        'user_agent': user_agent,
                        'is_active': True,
                        'last_activity': timezone.now()
                    }
                )

            # Check if password change is required
            if user.needs_password_change():
                messages.warning(request, 'Your password has expired. Please change it.')
                return redirect('accounts:change_password')

            messages.success(request, f'Welcome back, {user.get_full_name() or user.username}!')
            return redirect('healthcenter:home')
        else:
            # Handle failed login
            try:
                user = CustomUser.objects.get(username=username)
                user.increment_failed_login()

                LoginAttempt.objects.create(
                    username=username,
                    ip_address=ip_address,
                    user_agent=user_agent,
                    success=False,
                    failure_reason='Invalid credentials'
                )

                attempts_left = 5 - user.failed_login_attempts
                if attempts_left > 0:
                    messages.error(request, f'Invalid credentials. {attempts_left} attempts remaining.')
                else:
                    messages.error(request, 'Account locked due to too many failed attempts.')
            except CustomUser.DoesNotExist:
                messages.error(request, 'Invalid credentials.')
    else:
        form = SecureLoginForm()

    return render(request, 'accounts/login.html', {'form': form})


@login_required
def user_logout(request):
    """Logout view with session cleanup"""
    # Mark session as inactive
    session_key = request.session.session_key
    if session_key:
        UserSession.objects.filter(session_key=session_key).update(is_active=False)

    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('healthcenter:home')


class UserRegisterView(CreateView):
    """User registration view"""
    form_class = SecureUserCreationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('accounts:login')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('healthcenter:home')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Account created successfully! Please log in.')
        return response

    def form_invalid(self, form):
        messages.error(self.request, 'Please correct the errors below.')
        return super().form_invalid(form)


@login_required
def change_password(request):
    """Password change view"""
    if request.method == 'POST':
        form = SecurePasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()

            # Update last password change
            user.last_password_change = timezone.now()
            user.require_password_change = False
            user.save(update_fields=['last_password_change', 'require_password_change'])

            # Keep user logged in after password change
            update_session_auth_hash(request, user)

            messages.success(request, 'Your password has been changed successfully!')
            return redirect('accounts:profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = SecurePasswordChangeForm(request.user)

    return render(request, 'accounts/change_password.html', {'form': form})


@login_required
def user_profile(request):
    """User profile view"""
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('accounts:profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserProfileForm(instance=request.user)

    # Get recent login attempts
    recent_logins = LoginAttempt.objects.filter(
        username=request.user.username
    ).order_by('-timestamp')[:10]

    # Get active sessions
    active_sessions = UserSession.objects.filter(
        user=request.user,
        is_active=True
    ).order_by('-last_activity')

    context = {
        'form': form,
        'recent_logins': recent_logins,
        'active_sessions': active_sessions,
        'password_age': request.user.password_age_days(),
    }

    return render(request, 'accounts/profile.html', context)


@login_required
def terminate_session(request, session_id):
    """Terminate a specific session"""
    try:
        session = UserSession.objects.get(id=session_id, user=request.user)
        session.is_active = False
        session.save()
        messages.success(request, 'Session terminated successfully.')
    except UserSession.DoesNotExist:
        messages.error(request, 'Session not found.')

    return redirect('accounts:profile')
