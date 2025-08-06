import os
from contextlib import asynccontextmanager

import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.starlette import StarletteIntegration
from sentry_sdk.consts import VERSION
from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
import subprocess

if os.environ.get("PROFILE") == "1":
    import pyinstrument
    from pyinstrument.renderers.html import HTMLRenderer
    from pyinstrument.renderers.speedscope import SpeedscopeRenderer


opts = {"dsn": None}

if os.environ.get("NO_TRACES_SAMPLE_RATE") == "1":
    print("Setting traces_sample_rate=None")
    opts["traces_sample_rate"] = None


if os.environ.get("NO_SESSIONS") == "1":
    print("Disabling session tracking")
    opts["auto_session_tracking"] = False


if os.environ.get("DISABLE_INTEGRATIONS") == "1":
    print("Will disable FastAPI integration")
    opts["disabled_integrations"] = [FastApiIntegration, StarletteIntegration]


if os.environ.get("NO_INTEGRATIONS") == "1":
    print("Will disable ALL integrations")
    opts["auto_enabling_integrations"] = False
    opts["default_integrations"] = False


if os.environ.get("INIT_SENTRY") == "1":
    print("Initializing Sentry...")
    print("Options:", opts)
    sentry_sdk.init(**opts)
    print("sentry-sdk version:", VERSION)


@asynccontextmanager
async def lifespan(app):
    print("FastAPI application is starting...")
    if os.environ.get("INIT_SENTRY_LIFESPAN") == "1":
        print("Initializing Sentry from lifespan...")
        print("Options:", opts)
        sentry_sdk.init(**opts)
        print("sentry-sdk version:", VERSION)
    yield


app = FastAPI(lifespan=lifespan)

if os.environ.get("PROFILE") == "1":

    @app.middleware("http")
    async def profile_request(request, call_next):
        print("Profiling middleware running")
        """Profile the current request

        Taken from https://pyinstrument.readthedocs.io/en/latest/guide.html#profile-a-web-request-in-fastapi
        with small improvements.

        """
        profile_type_to_ext = {"html": "html", "speedscope": "speedscope.json"}
        profile_type_to_renderer = {
            "html": HTMLRenderer,
            "speedscope": SpeedscopeRenderer,
        }

        with pyinstrument.Profiler(interval=0.00000001, async_mode="enabled") as profiler:
            response = await call_next(request)

        profile_type = "html"
        extension = profile_type_to_ext[profile_type]
        renderer = profile_type_to_renderer[profile_type]()
        with open(f"profile.{extension}", "w") as out:
            out.write(profiler.output(renderer=renderer))
            print(f'Wrote profile.{extension}')

        return response


@app.get("/hello")
def hello():
    return PlainTextResponse("Hello, world!")


@app.get("/hello-async")
async def async_hello():
    return PlainTextResponse("Hello, async world!")
