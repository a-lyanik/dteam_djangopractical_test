from .models import RequestLog


class RequestLoggingMiddleware:
    """Middleware to log every incoming HTTP request."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Log the request
        RequestLog.objects.create(
            http_method=request.method,
            path=request.get_full_path()
        )
        return self.get_response(request)
