# Run servers and benchmarks for Sentry performance checks.
# Run the check against:
# - Django app (sync and async views) with and without Sentry SDK initialization.
# - FastAPI app (sync and async views) with and without Sentry SDK initialization.


function run_bench() {
    local name="$1"
    local url="$2"

    echo "Running benchmark for $name at $url (please wait)..."
    ab -t 20 -c 100 "$url" > ./bench_results/$name.txt
}

function killall() {
    echo "Killing all background processes..."
    kill -INT 0
}

trap 'killall' EXIT

# Run servers
PORT=9000 uv run ./d/main.py &
PORT=9001 uv run ./f/main.py &
INIT_SENTRY=1 PORT=9002 uv run ./d/main.py &
INIT_SENTRY=1 PORT=9003 uv run ./f/main.py &
INIT_SENTRY_LIFESPAN=1 PORT=9004 uv run ./f/main.py &

echo "Waiting for servers to start..."
sleep 2

# Run benchmarks
run_bench "django_sync_no_sentry" "http://127.0.0.1:9000/hello"
run_bench "django_async_no_sentry" "http://127.0.0.1:9000/hello-async"
run_bench "django_sync_with_sentry" "http://127.0.0.1:9002/hello"
run_bench "django_async_with_sentry" "http://127.0.0.1:9002/hello-async"

run_bench "fastapi_sync_no_sentry" "http://127.0.0.1:9001/hello"
run_bench "fastapi_async_no_sentry" "http://127.0.0.1:9001/hello-async"
run_bench "fastapi_sync_with_sentry" "http://127.0.0.1:9003/hello"
run_bench "fastapi_async_with_sentry" "http://127.0.0.1:9003/hello-async"
run_bench "fastapi_sync_with_sentry_lifespan" "http://127.0.0.1:9004/hello"
run_bench "fastapi_async_with_sentry_lifespan" "http://127.0.0.1:9004/hello-async"

echo ""
echo ""
echo "Benchmarks completed. Results saved in ./bench_results/"
echo ""
