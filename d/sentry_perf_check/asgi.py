import os

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sentry_perf_check.settings")

print("Starting Django ASGI application...")

application = get_asgi_application()
