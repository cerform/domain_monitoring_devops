#!/bin/bash
set -e

echo "Starting Flask backend..."
python app.py &

echo "Waiting for backend to start..."
sleep 5

echo "Running tests..."
pytest tests --maxfail=1 --disable-warnings -q
