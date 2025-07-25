# /// script
# dependencies = [
#   "django",
#   "sentry-sdk",
#   "uvicorn",
#   "uvloop",
#   "httptools",
# ]
# ///

import os

import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "sentry_perf_check.asgi:application",
        port=int(os.getenv("PORT")),
        access_log=False,
    )
