# accounts/middleware.py
from django.utils import translation

class PreferredLanguageMiddleware:
    """
    If user is authenticated and has preferred_language set,
    activate it for the duration of the request.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # activate user language if present
        user = getattr(request, "user", None)
        lang = None
        if user and user.is_authenticated:
            lang = getattr(user, "preferred_language", None)

        if lang:
            translation.activate(lang)
            request.LANGUAGE_CODE = lang

        response = self.get_response(request)

        # optional: deactivate or restore to default
        translation.deactivate()
        return response

class PreferredLanguageMiddleware:
    """
    Activate user's preferred_language (if set) for each request.
    Place this middleware after AuthenticationMiddleware.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # request.user is available after AuthenticationMiddleware
        user = getattr(request, "user", None)
        if user and user.is_authenticated:
            lang = getattr(user, "preferred_language", None)
            if lang:
                translation.activate(lang)
                request.LANGUAGE_CODE = lang
        response = self.get_response(request)
        return response