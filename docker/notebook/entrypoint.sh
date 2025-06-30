#!/bin/bash
set -e

echo "Starting marimo notebook server..."
cd /app/notebooks
exec marimo edit --host 0.0.0.0 --port 2718 --no-token
