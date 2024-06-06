# Start with the BuildKit image
FROM moby/buildkit:v0.9.3

# Install Python and pip
RUN apk update && apk add --no-cache \
    python3 \
    py3-pip \
    build-base \
    ca-certificates \
    curl \
    bash

# Install Flask
RUN pip3 install Flask

# Set the working directory
WORKDIR /app

# Copy the server code into the container
COPY server.py /app

# Expose port 5000
EXPOSE 5000

# Copy entrypoint script
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Run the entrypoint script
ENTRYPOINT ["/entrypoint.sh"]
