FROM gitpod/workspace-postgresql

# Install Redis.
RUN sudo apt-get update \
 && sudo apt-get install -y \
  redis-server socat \
 && sudo rm -rf /var/lib/apt/lists/*