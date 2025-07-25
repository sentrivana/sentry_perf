import os

import sentry_sdk

if os.environ.get("INIT_SENTRY") == "1":
    print("Initializing Sentry...")
    sentry_sdk.init()

ALLOWED_HOSTS = ["*"]

ROOT_URLCONF = "sentry_perf_check.urls"
