#!/usr/bin/env bash

exec gunicorn app:app -k uvicorn.workers.UvicornWorker --config /var/gunicorn/gunicorn.py -b 0.0.0.0:8000

#exec uvicorn app:app --host 0.0.0.0 --port 8003 --reload
