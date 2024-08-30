#!/bin/sh
if [ ! -d /login_app/venv ]; then \
    echo "[INFO] >> Installing dependencies, please wait..." && \
    python -m venv venv && \
    source venv/bin/activate && \
    pip install -r requirements.txt && \
    pip freeze > requirements.txt && \
    uvicorn main:app --host 0.0.0.0 --port 8002 --reload \
;else \
    echo "[INFO] >> Ready to launch server, checking new dependencies, please wait..." && \
    source venv/bin/activate && \
    pip install -r requirements.txt && \
    pip freeze > requirements.txt && \
    uvicorn main:app --host 0.0.0.0 --port 8002 --reload \
;fi