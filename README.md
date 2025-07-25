# sentry_perf

A repo to showcase the performance impact of a "bare" `sentry_sdk.init()` call on Django and FastAPI apps


## Contents

- `d` directory - sample Django app using Sentry SDK init function.
- `f` directory - sample FastAPI app using Sentry SDK init function.
- `bench_results` directory - a place to store benchmark results
- `run.sh` script - starts the servers with specific config
  and runs `ab` benchmarks against some HTTP endpoints.


## Usage

Simply call:
```sh
bash run.sh
```

and check the results in the `bench_results` directory.


## Setup

Both the Django and FastAPI apps are very simple and expose two simple "endpoints":
- `/hello` and
- `/hello-async`

Both setups are trimmed down to only relevant bits (no middlewares etc.).
Each one has a `main.py` file that runs a **Uvicorn** server (with `uvloop` and `httptools` for better performance)
against a relevant ASGI app with:
- access logs disabled and
- port configured via `PORT` env var.

Both apps call `sentry_sdk.init()` conditionally based on the presence of `INIT_SENTRY=1` env var.

Additionally the FastAPI app can call `sentry_sdk.init()` inside the `lifespan` function.
This is controlled with the `INIT_SENTRY_LIFESPAN=1` env var.


## Benchmark

For testing each endpoint I use Apache Benchmark with a time limit of `20` seconds
and concurrency set to `100`. Like this:
```sh
ab -t 20 -c 100 $URL
```

It's probably not the best measurement, but I noticed it's pretty consistent
and allows to compare results quite reliably.

This command is run against:

- Django app:
    - sync `/hello` endpoint:
        - without initializing Sentry and
        - with initializing Sentry in the settings module.
    - async `/hello-async` endpoint:
        - without initializing Sentry and
        - with initializing Sentry in the settings module.

- FastAPI app:
    - sync `/hello` endpoint:
        - without initializing Sentry,
        - with initializing Sentry in the global scope and
        - with initializing Sentry in the lifespan function.
    - async `/hello-async` endpoint:
        - without initializing Sentry,
        - with initializing Sentry in the global scope and
        - with initializing Sentry in the lifespan function.


## Customization

You can play around with different setups by taking advantage of the tooling that the `run.sh` script is using.
E.g. you might try and play around with the following env vars.

- `WEB_CONCURRENCY` - uvicorn honors this and spins up relevant number of workers for each server (1 by default).
- `UV_PYTHON` - `run.sh` uses `uv` to run the `main.py` scripts, so with this you can control the Python version that is used.


## Results

With Python `3.12.11` and 1 worker, on my machine I'm getting:
```sh
$ grep -R "Requests per" ./bench_results/workers_1/ | sort | column -t -s ":"
./bench_results/workers_1/django_async_no_sentry.txt              Requests per second      4153.79 [#/sec] (mean)
./bench_results/workers_1/django_async_with_sentry.txt            Requests per second      2020.24 [#/sec] (mean)
./bench_results/workers_1/django_sync_no_sentry.txt               Requests per second      3617.33 [#/sec] (mean)
./bench_results/workers_1/django_sync_with_sentry.txt             Requests per second      1855.39 [#/sec] (mean)
./bench_results/workers_1/fastapi_async_no_sentry.txt             Requests per second      20804.47 [#/sec] (mean)
./bench_results/workers_1/fastapi_async_with_sentry_lifespan.txt  Requests per second      7140.86 [#/sec] (mean)
./bench_results/workers_1/fastapi_async_with_sentry.txt           Requests per second      4729.49 [#/sec] (mean)
./bench_results/workers_1/fastapi_sync_no_sentry.txt              Requests per second      10485.90 [#/sec] (mean)
./bench_results/workers_1/fastapi_sync_with_sentry_lifespan.txt   Requests per second      5239.53 [#/sec] (mean)
./bench_results/workers_1/fastapi_sync_with_sentry.txt            Requests per second      3411.95 [#/sec] (mean)
```

for 9 workers, I'm getting:
```sh
$ grep -R "Requests per" ./bench_results/workers_9 | sort | column -t -s ":"
./bench_results/workers_9/django_async_no_sentry.txt              Requests per second      10786.02 [#/sec] (mean)
./bench_results/workers_9/django_async_with_sentry.txt            Requests per second      5737.26 [#/sec] (mean)
./bench_results/workers_9/django_sync_no_sentry.txt               Requests per second      9676.25 [#/sec] (mean)
./bench_results/workers_9/django_sync_with_sentry.txt             Requests per second      5364.70 [#/sec] (mean)
./bench_results/workers_9/fastapi_async_no_sentry.txt             Requests per second      25284.58 [#/sec] (mean)
./bench_results/workers_9/fastapi_async_with_sentry_lifespan.txt  Requests per second      25560.71 [#/sec] (mean)
./bench_results/workers_9/fastapi_async_with_sentry.txt           Requests per second      19935.31 [#/sec] (mean)
./bench_results/workers_9/fastapi_sync_no_sentry.txt              Requests per second      29257.82 [#/sec] (mean)
./bench_results/workers_9/fastapi_sync_with_sentry_lifespan.txt   Requests per second      16774.62 [#/sec] (mean)
./bench_results/workers_9/fastapi_sync_with_sentry.txt            Requests per second      12471.81 [#/sec] (mean)
```