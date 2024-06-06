#!/bin/bash

# Function to handle termination signals
terminate() {
    echo "Termination signal received, shutting down..."
    # Perform any cleanup actions here
    kill -SIGTERM $buildkitd_pid
    kill -SIGTERM $flask_pid
    wait $buildkitd_pid
    wait $flask_pid
    exit 0
}

# Trap termination signals
trap terminate SIGTERM SIGINT

# Start BuildKit daemon
buildkitd &
buildkitd_pid=$!

# Wait for BuildKit to be ready
while [ ! -S /run/buildkit/buildkitd.sock ]; do
  sleep 1
done

# Modify ~/.docker/config.json to change "credsStore" to "credStore"
if [ -f ~/.docker/config.json ]; then
  sed -i 's/"credsStore"/"credStore"/g' ~/.docker/config.json
fi

# Start Flask server
python3 /app/server.py &
flask_pid=$!

# Wait for Flask server to exit
wait $flask_pid
