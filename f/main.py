import os

import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        app="asgi:app",
        port=int(os.getenv("PORT")),
        access_log=False,
    )
