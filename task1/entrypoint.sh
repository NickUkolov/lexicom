#!/bin/bash
exec uvicorn --host="$FASTAPI_HOST" --port="$FASTAPI_PORT" --log-level debug main:app