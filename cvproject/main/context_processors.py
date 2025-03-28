from django.conf import settings


def settings_context(request):
    """
    Injects all Django settings into the template context.
    """
    return {"settings": settings}
