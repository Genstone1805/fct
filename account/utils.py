import os
from django.conf import settings
from django.utils import timezone


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