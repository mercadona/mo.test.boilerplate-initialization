import os

from fastapi import FastAPI
from monitoring.contrib.fastapi.fastapi import instrument

SENTRY_DSN = os.environ.get("SENTRY_DSN")

app = FastAPI()
instrument(app)


@app.get("/health/")
async def health() -> str:
    return "OK"
