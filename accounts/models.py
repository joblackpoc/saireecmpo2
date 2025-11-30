from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from datetime import timedelta


class CustomUser(AbstractUser):
    """
    Custom User model with enhanced security features
    """
    # Additional fields
    phone = models.CharField(max_length=20, blank=True, help_text="Contact phone number")
    date_of_birth = models.DateField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)

    # Security fields
    failed_login_attempts = models.IntegerField(default=0, help_text="Number of failed login attempts")
    account_locked_until = models.DateTimeField(null=True, blank=True, help_text="Account locked until this time")
    last_password_change = models.DateTimeField(auto_now_add=True, help_text="Last time password was changed")
    require_password_change = models.BooleanField(default=False, help_text="Force password change on next login")

    # Two-factor authentication
    two_factor_enabled = models.BooleanField(default=False, help_text="Enable two-factor authentication")
    two_factor_secret = models.CharField(max_length=32, blank=True, help_text="2FA secret key")

    # Activity tracking
    last_login_ip = models.GenericIPAddressField(null=True, blank=True, help_text="Last login IP address")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ['-date_joined']

    def __str__(self):
        return f"{self.username} ({self.get_full_name() or self.email})"

    def is_account_locked(self):
        """Check if account is currently locked"""
        if self.account_locked_until:
            if timezone.now() < self.account_locked_until:
                return True
            else:
                # Unlock account if lock period has passed
                self.account_locked_until = None
                self.failed_login_attempts = 0
                self.save(update_fields=['account_locked_until', 'failed_login_attempts'])
        return False

    def increment_failed_login(self):
        """Increment failed login attempts and lock account if necessary"""
        self.failed_login_attempts += 1

        # Lock account after 5 failed attempts for 30 minutes
        if self.failed_login_attempts >= 5:
            self.account_locked_until = timezone.now() + timedelta(minutes=30)

        self.save(update_fields=['failed_login_attempts', 'account_locked_until'])

    def reset_failed_login(self):
        """Reset failed login attempts after successful login"""
        self.failed_login_attempts = 0
        self.account_locked_until = None
        self.save(update_fields=['failed_login_attempts', 'account_locked_until'])

    def password_age_days(self):
        """Get password age in days"""
        if self.last_password_change:
            return (timezone.now() - self.last_password_change).days
        return 0

    def needs_password_change(self, max_age_days=90):
        """Check if password change is required (default 90 days)"""
        return self.require_password_change or self.password_age_days() > max_age_days


class LoginAttempt(models.Model):
    """
    Track all login attempts for security monitoring
    """
    username = models.CharField(max_length=150)
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField(blank=True)
    success = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    failure_reason = models.CharField(max_length=255, blank=True)

    class Meta:
        verbose_name = "Login Attempt"
        verbose_name_plural = "Login Attempts"
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['-timestamp']),
            models.Index(fields=['username', '-timestamp']),
            models.Index(fields=['ip_address', '-timestamp']),
        ]

    def __str__(self):
        status = "Success" if self.success else "Failed"
        return f"{status} - {self.username} from {self.ip_address} at {self.timestamp}"


class UserSession(models.Model):
    """
    Track active user sessions for security
    """
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sessions')
    session_key = models.CharField(max_length=40, unique=True)
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_activity = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "User Session"
        verbose_name_plural = "User Sessions"
        ordering = ['-last_activity']

    def __str__(self):
        return f"{self.user.username} - {self.ip_address} ({self.created_at})"
