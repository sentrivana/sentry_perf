#!/bin/bash
set -eu

# Run servers and benchmarks for Sentry performance checks.
# Run the check against:
# - Django app (sync and async views) with and without Sentry SDK initialization.
# - FastAPI app (sync and async views)
#   without Sentry SDK initialization and with Sentry SDK initialization (both global and in lifespan function).

function run_bench() {
    local name="$1"
    local url="$2"
    local workers=${WEB_CONCURRENCY:-1}
    local dir="./bench_results/workers_${workers}"

    mkdir -p "$dir"

    echo "Running benchmark for $name at $url (please wait)..."
    ab -t 20 -c 100 "$url" > "$dir/$name.txt"
}

function killservers() {
    echo "Killing all background processes..."
    kill -INT $(jobs -p)
    wait
}

trap 'killservers' EXIT

# Run servers
#rm -rf d.env
#python3 -m venv d.env
#. d.env/bin/activate
#pip install -e ../sentry-python
#pip install django uvicorn uvloop httptools pyinstrument py-spy

rm -rf f.env
python3 -m venv f.env
. f.env/bin/activate
pip install -e ../sentry-python
pip install fastapi uvicorn uvloop httptools pyinstrument py-spy


INIT_SENTRY=1 PORT=9000 f.env/bin/python ./f/main.py &
PORT=9001 f.env/bin/python ./f/main.py &
INIT_SENTRY_LIFESPAN=1 PORT=9002 f.env/bin/python ./f/main.py &
#PORT=9003 d.env/bin/python ./d/main.py &
#INIT_SENTRY=1 PORT=9004 d.env/bin/python ./d/main.py &

echo "Waiting for servers to start..."
sleep 5

# Run benchmarks
run_bench "fastapi_sync_with_sentry" "http://127.0.0.1:9000/hello"
run_bench "fastapi_async_with_sentry" "http://127.0.0.1:9000/hello-async"

run_bench "fastapi_sync_no_sentry" "http://127.0.0.1:9001/hello"
run_bench "fastapi_async_no_sentry" "http://127.0.0.1:9001/hello-async"

run_bench "fastapi_sync_with_sentry_lifespan" "http://127.0.0.1:9002/hello"
run_bench "fastapi_async_with_sentry_lifespan" "http://127.0.0.1:9002/hello-async"

#run_bench "django_sync_no_sentry" "http://127.0.0.1:9003/hello"
#run_bench "django_async_no_sentry" "http://127.0.0.1:9003/hello-async"

#run_bench "django_sync_with_sentry" "http://127.0.0.1:9004/hello"
#run_bench "django_async_with_sentry" "http://127.0.0.1:9004/hello-async"


echo ""
echo ""
echo "Benchmarks completed. Results saved in ./bench_results/"
echo ""
