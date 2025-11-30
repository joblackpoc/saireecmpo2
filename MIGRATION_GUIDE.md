# Accounts App Migration Guide

## Overview
The accounts app has been successfully integrated with custom user authentication and security features. However, the database migration requires manual steps because we're changing the user model after the initial database setup.

## What's Been Completed

✅ **Configuration Files Updated:**
- Added `accounts` to INSTALLED_APPS in [settings.py](core/settings.py)
- Set `AUTH_USER_MODEL = 'accounts.CustomUser'` in [settings.py](core/settings.py)
- Added authentication URLs to [core/urls.py](core/urls.py)
- Configured session security settings

✅ **Models Created:**
- `CustomUser` - Enhanced user model with security features
- `LoginAttempt` - Track all login attempts for security monitoring
- `UserSession` - Track active user sessions

✅ **Views and Forms:**
- Secure login with failed attempt tracking and account lockout
- User registration with strong password validation
- User profile management
- Password change functionality
- Session management

✅ **Templates Created:**
- [login.html](templates/accounts/login.html) - Modern login page
- [register.html](templates/accounts/register.html) - Registration form
- [profile.html](templates/accounts/profile.html) - User profile with security info
- [change_password.html](templates/accounts/change_password.html) - Password change form

✅ **URL Patterns:**
- `/accounts/login/` - User login
- `/accounts/logout/` - User logout
- `/accounts/register/` - User registration
- `/accounts/profile/` - User profile
- `/accounts/change-password/` - Change password
- `/accounts/terminate-session/<id>/` - Terminate specific session

## Migration Steps Required

### Step 1: Stop All Django Processes
Make sure no Django development server or shell is running:
- Close all terminal windows running `python manage.py runserver`
- Close any Django shells
- Close VSCode if it has Python extensions that might lock the database

### Step 2: Backup Current Database (Optional)
```bash
cd e:\PROJECT\saireecmpo
copy db.sqlite3 db.sqlite3.backup
```

### Step 3: Delete Old Database
Since we're changing the user model, we need a fresh database:
```bash
cd e:\PROJECT\saireecmpo
del db.sqlite3
```

### Step 4: Run Migrations
```bash
cd e:\PROJECT\saireecmpo
python manage.py migrate
```

This will create all tables including:
- accounts_customuser
- accounts_loginattempt
- accounts_usersession
- All other Django tables (admin, auth, sessions, etc.)

### Step 5: Create Superuser
Create an admin account to access the system:
```bash
python manage.py createsuperuser
```

Follow the prompts to set:
- Username
- Email address
- Password (must meet security requirements: 8+ chars, uppercase, lowercase, number, special character)

### Step 6: Run Development Server
```bash
python manage.py runserver
```

### Step 7: Test the System
1. **Login Page:** http://127.0.0.1:8000/accounts/login/
2. **Register Page:** http://127.0.0.1:8000/accounts/register/
3. **Profile Page:** http://127.0.0.1:8000/accounts/profile/ (after login)
4. **Admin Panel:** http://127.0.0.1:8000/secure-admin/

## Security Features Implemented

### 1. Account Lockout
- After 5 failed login attempts, account is locked for 30 minutes
- Prevents brute force attacks

### 2. Password Requirements
- Minimum 8 characters
- At least one uppercase letter (A-Z)
- At least one lowercase letter (a-z)
- At least one number (0-9)
- At least one special character (!@#$%^&*...)

### 3. Password Aging
- Tracks when password was last changed
- Configurable password expiration (default: 90 days)
- Force password change flag

### 4. Session Management
- Track all active sessions per user
- View session details (IP, user agent, last activity)
- Ability to terminate specific sessions
- Configurable session expiry (default: 2 weeks)

### 5. Login Attempt Tracking
- Log all login attempts (successful and failed)
- Track IP addresses and user agents
- Record failure reasons
- Indexed for fast queries

### 6. Security Headers
- HTTP-only cookies
- CSRF protection
- XSS filtering
- Content type sniffing prevention
- X-Frame-Options: DENY

### 7. Two-Factor Authentication Support
- Database fields ready for 2FA implementation
- `two_factor_enabled` boolean flag
- `two_factor_secret` for storing secret key

## Admin Features

Access the admin panel at: http://127.0.0.1:8000/secure-admin/

### CustomUser Admin
- View all user accounts
- See security fields (failed attempts, lockout status)
- View last login IP and 2FA status
- Filter by staff, superuser, active status

### LoginAttempt Admin (Read-Only)
- View all login attempts
- Filter by success/failure
- Search by username or IP
- Ordered by timestamp

### UserSession Admin (Read-Only)
- View all user sessions
- Filter by active/inactive status
- Search by username or IP
- Ordered by last activity

## URL Structure

### Accounts URLs
- `accounts/login/` - Login page
- `accounts/logout/` - Logout (redirects to login)
- `accounts/register/` - Registration page
- `accounts/profile/` - User profile (requires login)
- `accounts/change-password/` - Change password (requires login)
- `accounts/terminate-session/<id>/` - Terminate session (requires login)

### Other URLs
- `/` - Home page (healthcenter app)
- `secure-admin/` - Real admin panel
- `admin/` - Honeypot (fake admin to catch attackers)
- `ckeditor5/` - CKEditor file upload

## Next Steps (Optional Enhancements)

1. **Email Verification**
   - Add email verification on registration
   - Send password reset emails

2. **Two-Factor Authentication**
   - Implement TOTP-based 2FA
   - Add QR code generation for secret

3. **Password Reset**
   - Add "Forgot Password" functionality
   - Send reset links via email

4. **Social Login**
   - Add Google/Facebook OAuth
   - Use django-allauth

5. **Rate Limiting**
   - Add django-ratelimit
   - Limit login attempts per IP

6. **Activity Logs**
   - Log all user actions
   - Create audit trail

## Troubleshooting

### Migration Error: "InconsistentMigrationHistory"
**Problem:** Database already has migrations applied with the old user model.

**Solution:** Delete the database and run migrations fresh (see Step 3 above).

### "Manager isn't available; 'auth.User' has been swapped"
**Problem:** Trying to use old User model after switching to CustomUser.

**Solution:**
- Use `from accounts.models import CustomUser` instead of `from django.contrib.auth.models import User`
- Or use `from django.contrib.auth import get_user_model()` and `User = get_user_model()`

### Session Security Warnings
**Problem:** SESSION_COOKIE_SECURE is False.

**Solution:** This is OK for development. In production:
```python
SESSION_COOKIE_SECURE = True  # Only send cookies over HTTPS
```

### Admin Namespace Warning
**Problem:** `URL namespace 'admin' isn't unique`

**Solution:** This is expected. We have:
- `/admin/` - Honeypot (fake admin)
- `/secure-admin/` - Real admin panel

## File Reference

### Models
- [accounts/models.py](accounts/models.py) - CustomUser, LoginAttempt, UserSession

### Views
- [accounts/views.py](accounts/views.py) - All authentication views

### Forms
- [accounts/forms.py](accounts/forms.py) - Login, registration, profile forms

### URLs
- [accounts/urls.py](accounts/urls.py) - Accounts URL patterns
- [core/urls.py](core/urls.py) - Main URL configuration

### Templates
- [templates/accounts/login.html](templates/accounts/login.html)
- [templates/accounts/register.html](templates/accounts/register.html)
- [templates/accounts/profile.html](templates/accounts/profile.html)
- [templates/accounts/change_password.html](templates/accounts/change_password.html)

### Configuration
- [core/settings.py](core/settings.py) - Django settings with security configuration

### Admin
- [accounts/admin.py](accounts/admin.py) - Admin configuration for CustomUser, LoginAttempt, UserSession

## Support

If you encounter any issues:
1. Check the migration steps above
2. Ensure all processes using the database are stopped
3. Verify Python and Django versions are compatible
4. Check the Django development server output for errors

---

**Status:** Ready for migration. Follow steps above to complete the integration.
