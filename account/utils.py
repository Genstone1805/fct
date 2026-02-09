import os
from django.conf import settings
from django.utils import timezone
from contextlib import suppress
from django.core.mail import send_mail

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
    # Send email with credentials
    subject = "Welcome to First Class Transfer - Your Login Credentials"  
    permissions_text = ", ".join(permissions) if permissions else "None"
    role_text = "Administrator" if user.is_superuser else "Staff"

    message = f"""
        Hello {user.full_name or 'there'},

        Welcome to First Class Transfer! Your account has been created successfully.

        Here are your login credentials:

        Email: {user.email}
        Password: {generated_password}

        Your Role: {role_text}
        Your Permissions: {permissions_text}
        
        visit https://firstclasstransfers.eu/admin/login to login

        Best regards,
        First Class Transfer Team
    """
    with suppress(Exception):
        send_mail(
            subject,
            message,
            settings.EMAIL_FROM,
            [user.email],
            fail_silently=False,
        )

def signup_email_to_admin(user, permissions, admin):
    # Send email with credentials
    subject = "New User Account Created Successfully"  
    permissions_text = ", ".join(permissions) if permissions else "None"
    role_text = "Administrator" if user.is_superuser else "Staff"

    message = f"""
        Hello,

        This is to notify you that a new user account has been successfully created on the First Class Transfer platform.

        User Details

        Name: {user.full_name}

        Email: {user.email}

        Assigned Role: {role_text}

        Permissions: {permissions_text}
        
        Created By: {admin.full_name}

        The user has been provisioned with initial login credentials and instructed to update their password upon first login to maintain security compliance.

        No further action is required at this time unless changes to roles or permissions are needed.

        If you have any questions or require adjustments, please proceed through the appropriate administrative channels.

        Best regards,
        First Class Transfer Team
    """
    with suppress(Exception):
        send_mail(
            subject,
            message,
            settings.EMAIL_FROM,
            [settings.EMAIL_FROM],
            fail_silently=False,
        )