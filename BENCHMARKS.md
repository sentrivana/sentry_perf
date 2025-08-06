### Normal operation

```
fastapi_async_no_sentry.txt             Requests per second      17007.83 [#/sec] (mean)
fastapi_async_with_sentry_lifespan.txt  Requests per second      6637.40 [#/sec] (mean)
fastapi_async_with_sentry.txt           Requests per second      4384.14 [#/sec] (mean)
fastapi_sync_no_sentry.txt              Requests per second      8136.62 [#/sec] (mean)
fastapi_sync_with_sentry_lifespan.txt   Requests per second      4469.85 [#/sec] (mean)
fastapi_sync_with_sentry.txt            Requests per second      2962.05 [#/sec] (mean)
```

### :star: Without Starlette/FastAPI integration

```
fastapi_async_no_sentry.txt             Requests per second      16504.15 [#/sec] (mean)
fastapi_async_with_sentry_lifespan.txt  Requests per second      17329.28 [#/sec] (mean)
fastapi_async_with_sentry.txt           Requests per second      16943.89 [#/sec] (mean)
fastapi_sync_no_sentry.txt              Requests per second      8480.18 [#/sec] (mean)
fastapi_sync_with_sentry_lifespan.txt   Requests per second      8425.28 [#/sec] (mean)
fastapi_sync_with_sentry.txt            Requests per second      8389.11 [#/sec] (mean)
```

### No `logger.debug` in ASGI

```
fastapi_async_no_sentry.txt             Requests per second      16870.62 [#/sec] (mean)
fastapi_async_with_sentry_lifespan.txt  Requests per second      8132.47 [#/sec] (mean)
fastapi_async_with_sentry.txt           Requests per second      4807.12 [#/sec] (mean)
fastapi_sync_no_sentry.txt              Requests per second      7891.27 [#/sec] (mean)
fastapi_sync_with_sentry_lifespan.txt   Requests per second      5293.36 [#/sec] (mean)
fastapi_sync_with_sentry.txt            Requests per second      3361.36 [#/sec] (mean)
```

### Against `potel-base`

```
fastapi_async_no_sentry.txt             Requests per second      16572.41 [#/sec] (mean)
fastapi_async_with_sentry_lifespan.txt  Requests per second      6714.67 [#/sec] (mean)
fastapi_async_with_sentry.txt           Requests per second      3923.62 [#/sec] (mean)
fastapi_sync_no_sentry.txt              Requests per second      7819.74 [#/sec] (mean)
fastapi_sync_with_sentry_lifespan.txt   Requests per second      4359.10 [#/sec] (mean)
fastapi_sync_with_sentry.txt            Requests per second      2834.32 [#/sec] (mean)
```

### Without session tracking

```
fastapi_async_no_sentry.txt             Requests per second      16916.86 [#/sec] (mean)
fastapi_async_with_sentry_lifespan.txt  Requests per second      7226.73 [#/sec] (mean)
fastapi_async_with_sentry.txt           Requests per second      4538.16 [#/sec] (mean)
fastapi_sync_no_sentry.txt              Requests per second      8312.31 [#/sec] (mean)
fastapi_sync_with_sentry_lifespan.txt   Requests per second      4893.85 [#/sec] (mean)
fastapi_sync_with_sentry.txt            Requests per second      3270.49 [#/sec] (mean)
```

### Removing different monkeypatches in `StarletteIntegration`

See which of the four monkeypatches (`middlewares`, `asgi_app`, `request_response`, `templates`) makes a difference.

* Not patching `middlewares` makes no big difference
* Not patching `request_response` makes no big difference
* Not patching `templates` makes no big difference
* Not patching `asgi_app` makes a HUGE difference (see table below)

```
fastapi_async_no_sentry.txt             Requests per second      16520.57 [#/sec] (mean)
fastapi_async_with_sentry_lifespan.txt  Requests per second      16845.35 [#/sec] (mean)
fastapi_async_with_sentry.txt           Requests per second      6602.33 [#/sec] (mean)
fastapi_sync_no_sentry.txt              Requests per second      8457.25 [#/sec] (mean)
fastapi_sync_with_sentry_lifespan.txt   Requests per second      8054.90 [#/sec] (mean)
fastapi_sync_with_sentry.txt            Requests per second      4144.70 [#/sec] (mean)
```

Unsurprisingly, it's the middleware that's causing the biggest performance hit.
