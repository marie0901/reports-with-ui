#!/bin/bash

# Function to kill background processes on exit
cleanup() {
    echo "Stopping servers..."
    kill $(jobs -p) 2>/dev/null
}
trap cleanup EXIT

# Start Backend
echo "Starting Backend..."
source api/venv/bin/activate
uvicorn api.index:app --reload --port 8000 &
BACKEND_PID=$!

# Wait for backend to start
sleep 2

# Start Frontend
echo "Starting Frontend..."
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
npm run dev

# Wait for processes
wait $BACKEND_PID
