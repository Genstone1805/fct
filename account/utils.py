import os
from django.conf import settings
from django.utils import timezone
from contextlib import suppress

from booking.emails import _send_html_email

def get_activity_log_path():
    """Get the path to the activity log file."""
    logs_dir = getattr(settings, 'LOGS_DIR', settings.BASE_DIR / 'logs')
    return os.path.join(logs_dir, 'user_activity.log')


def get_client_ip(request):
    """Extract client IP address from request."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR', 'unknown')


def log_user_activity(user, message, request=None):
    """Log user activity to the user's activity_log field and to a log file."""
    timestamp = timezone.now().strftime('%Y-%m-%d %H:%M:%S')
    ip_address = get_client_ip(request) if request else 'unknown'
    log_entry = f"[{timestamp}] {message}"

    # Save to user's activity_log field
    user.activity_log.append(log_entry)
    user.save(update_fields=['activity_log'])

    # Write to log file with IP address
    file_log_entry = f"[{timestamp}] [{user.full_name}] [{user.email}] [IP: {ip_address}] {message}\n"
    log_path = get_activity_log_path()

    os.makedirs(os.path.dirname(log_path), exist_ok=True)
    with open(log_path, 'a', encoding='utf-8') as f:
        f.write(file_log_entry)
        
def signup_email_to_user(user, permissions, generated_password):
    subject = "Welcome to First Class Transfer - Your Login Credentials"
    permissions_text = ", ".join(permissions) if permissions else "None"
    role_text = "Administrator" if user.is_superuser else "Staff"

    greeting = f"Hello {user.full_name or 'there'}"
    message = (
        "Welcome to First Class Transfers! Your account has been created successfully."
        "<br><br>Please visit the link below to log in:"
        "<br><a href='https://firstclasstransfers.eu/admin/login'>https://firstclasstransfers.eu/admin/login</a>"
    )
    detail = (
        f"<strong>Email:</strong> {user.email}<br>"
        f"<strong>Password:</strong> {generated_password}<br>"
        f"<strong>Role:</strong> {role_text}<br>"
        f"<strong>Permissions:</strong> {permissions_text}"
    )

    with suppress(Exception):
        _send_html_email(subject, greeting, message, detail, user.email)


def signup_email_to_admin(user, permissions, admin):
    subject = "New User Account Created Successfully"
    permissions_text = ", ".join(permissions) if permissions else "None"
    role_text = "Administrator" if user.is_superuser else "Staff"

    greeting = "Hello Admin"
    message = (
        "A new user account has been successfully created on the First Class Transfers platform."
        "<br><br>The user has been provisioned with initial login credentials and instructed "
        "to update their password upon first login."
        "<br><br>No further action is required unless changes to roles or permissions are needed."
    )
    detail = (
        f"<strong>Name:</strong> {user.full_name}<br>"
        f"<strong>Email:</strong> {user.email}<br>"
        f"<strong>Role:</strong> {role_text}<br>"
        f"<strong>Permissions:</strong> {permissions_text}<br>"
        f"<strong>Created By:</strong> {admin.full_name}"
    )

    with suppress(Exception):
        _send_html_email(subject, greeting, message, detail, settings.EMAIL_FROM)