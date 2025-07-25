# /// script
# dependencies = [
#   "django",
#   "sentry-sdk",
#   "uvicorn[standard]",
# ]
# ///

import os

import uvicorn

config = uvicorn.Config(
    app="sentry_perf_check.asgi:application",
    port=int(os.getenv("PORT")),
    workers=1,
    access_log=False,
)
server = uvicorn.Server(config)
server.run()
