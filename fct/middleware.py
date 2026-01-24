import logging
import time
import json
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger('request_logger')


class RequestResponseLoggingMiddleware(MiddlewareMixin):
    """
    Middleware to log all HTTP requests and responses.
    Logs method, path, status code, duration, IP address, and user.
    """

    def process_request(self, request):
        request._start_time = time.time()
        request._request_body = None

        # Capture request body for POST/PUT/PATCH
        if request.method in ['POST', 'PUT', 'PATCH']:
            try:
                if request.content_type and 'json' in request.content_type:
                    request._request_body = request.body.decode('utf-8')
            except Exception:
                pass

    def process_response(self, request, response):
        # Calculate duration
        duration = 0
        if hasattr(request, '_start_time'):
            duration = round((time.time() - request._start_time) * 1000, 2)

        # Get client IP
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR', 'unknown')

        # Get user
        user = 'anonymous'
        if hasattr(request, 'user') and request.user.is_authenticated:
            user = str(request.user)

        # Determine log level based on status code
        status_code = response.status_code
        if status_code >= 500:
            log_level = logging.ERROR
            status_type = 'ERROR'
        elif status_code >= 400:
            log_level = logging.WARNING
            status_type = 'WARNING'
        else:
            log_level = logging.INFO
            status_type = 'SUCCESS'

        # Build log message
        log_message = (
            f"{status_type} | {request.method} {request.path} | "
            f"Status: {status_code} | Duration: {duration}ms | "
            f"IP: {ip} | User: {user}"
        )

        # Add query parameters if present
        if request.GET:
            log_message += f" | Query: {dict(request.GET)}"

        # Add request body for non-GET requests (truncated)
        if hasattr(request, '_request_body') and request._request_body:
            body_preview = request._request_body[:500]
            if len(request._request_body) > 500:
                body_preview += '...[truncated]'
            log_message += f" | Body: {body_preview}"

        logger.log(log_level, log_message)

        return response

    def process_exception(self, request, exception):
        # Get client IP
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR', 'unknown')

        # Get user
        user = 'anonymous'
        if hasattr(request, 'user') and request.user.is_authenticated:
            user = str(request.user)

        logger.error(
            f"EXCEPTION | {request.method} {request.path} | "
            f"IP: {ip} | User: {user} | "
            f"Exception: {type(exception).__name__}: {str(exception)}"
        )
        return None
