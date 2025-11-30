from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, LoginAttempt, UserSession


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """Custom user admin with security fields"""
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active', 'failed_login_attempts', 'last_login')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'two_factor_enabled')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('-date_joined',)

    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('phone', 'date_of_birth', 'profile_picture')}),
        ('Security', {'fields': ('failed_login_attempts', 'account_locked_until', 'last_password_change', 'require_password_change', 'last_login_ip')}),
        ('Two-Factor Auth', {'fields': ('two_factor_enabled', 'two_factor_secret')}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Info', {'fields': ('email', 'first_name', 'last_name', 'phone')}),
    )


@admin.register(LoginAttempt)
class LoginAttemptAdmin(admin.ModelAdmin):
    """Login attempt admin"""
    list_display = ('username', 'ip_address', 'success', 'timestamp', 'failure_reason')
    list_filter = ('success', 'timestamp')
    search_fields = ('username', 'ip_address')
    ordering = ('-timestamp',)
    readonly_fields = ('username', 'ip_address', 'user_agent', 'success', 'timestamp', 'failure_reason')

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(UserSession)
class UserSessionAdmin(admin.ModelAdmin):
    """User session admin"""
    list_display = ('user', 'ip_address', 'is_active', 'created_at', 'last_activity')
    list_filter = ('is_active', 'created_at')
    search_fields = ('user__username', 'ip_address')
    ordering = ('-last_activity',)
    readonly_fields = ('user', 'session_key', 'ip_address', 'user_agent', 'created_at', 'last_activity')

    def has_add_permission(self, request):
        return False
