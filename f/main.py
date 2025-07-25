# /// script
# dependencies = [
#   "fastapi",
#   "sentry-sdk",
#   "uvicorn[standard]",
# ]
# ///

import os

import uvicorn

config = uvicorn.Config(
    app="asgi:app",
    port=int(os.getenv("PORT")),
    workers=1,
    access_log=False,
)
server = uvicorn.Server(config)
server.run()
