#!/bin/sh
if [ -n "$UVICORN_RELOAD" ]; then
    RELOAD=--reload
fi
uvicorn --host=0.0.0.0 --port 9000 --proxy-headers --log-level=info --ws=none $RELOAD backend.main:app
