#!/bin/bash
# Write DeepTutor's JSON settings from the Railway variables, then hand off to
# the image's own entrypoint (which drops to the unprivileged deeptutor user).
set -e
cd /app
PYTHONPATH=/app DEEPTUTOR_IGNORE_PROCESS_ENV_OVERRIDES=1 python /opt/railway/railway-setup.py
exec /app/entrypoint.sh "$@"
