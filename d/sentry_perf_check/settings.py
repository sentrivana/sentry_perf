import os

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.consts import VERSION

if os.environ.get("PROFILE") == "1":
    import pyinstrument

opts = {}

if os.environ.get("NO_TRACES_SAMPLE_RATE") == "1":
    print("Setting traces_sample_rate=None")
    opts["traces_sample_rate"] = None

if os.environ.get("NO_SESSIONS") == "1":
    print("Disabling session tracking")
    opts["auto_session_tracking"] = False


if os.environ.get("DISABLE_INTEGRATIONS") == "1":
    print("Will disable Django integration")
    opts["disabled_integrations"] = [DjangoIntegration]


if os.environ.get("INIT_SENTRY") == "1":
    print("Initializing Sentry...")
    print("Options:", opts)
    sentry_sdk.init(**opts)
    print("sentry-sdk version:", VERSION)

ALLOWED_HOSTS = ["*"]

ROOT_URLCONF = "sentry_perf_check.urls"
