import os
from contextlib import asynccontextmanager

import sentry_sdk
from fastapi import FastAPI
from fastapi.responses import PlainTextResponse

if os.environ.get("INIT_SENTRY") == "1":
    print("Initializing Sentry...")
    sentry_sdk.init()


@asynccontextmanager
async def lifespan(app):
    print("FastAPI application is starting...")
    if os.environ.get("INIT_SENTRY_LIFESPAN") == "1":
        print("Initializing Sentry from lifespan...")
        sentry_sdk.init()
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/hello")
def hello():
    return PlainTextResponse("Hello, world!")


@app.get("/hello-async")
async def async_hello():
    return PlainTextResponse("Hello, async world!")
