import pytz
from django.utils import timezone as tz
from django.shortcuts import redirect

class TimezoneMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        tz_name = request.session.get('user_timezone')
        if tz_name:
            try:
                user_tz = pytz.timezone(tz_name)
                tz.activate(user_tz)
            except pytz.UnknownTimeZoneError:
                tz.deactivate()
        else:
            tz.deactivate()
        return self.get_response(request)

class AuthRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        # Пути, не требующие аутентификации
        exempt_paths = [
            '/accounts/login/',
            '/signup/',
            '/',
            '/media/',
            '/static/',
        ]

        for path in exempt_paths:
            if request.path.startswith(path):
                return None

        if request.user.is_authenticated:
            return None

        return redirect('login')