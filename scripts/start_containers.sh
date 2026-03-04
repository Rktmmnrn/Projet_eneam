#!/usr/bin/env bash
set -euo pipefail

echo "Helper: start Docker Engine or enable Podman socket, then run docker-compose"

usage() {
  cat <<EOF
Usage: $0 [docker|podman|compose]
  docker  - Start system Docker (requires sudo)
  podman  - Enable user podman.socket and prints DOCKER_HOST export
  compose - Run 'docker-compose up --build' (uses current environment)
EOF
}

if [ "$#" -lt 1 ]; then
  usage
  exit 1
fi

case "$1" in
  docker)
    echo "Starting Docker Engine (requires sudo)..."
    sudo systemctl enable --now docker
    echo "Adding current user to 'docker' group (may require logout/login)..."
    sudo usermod -aG docker "$USER" || true
    echo "Verify: docker version"
    docker version || true
    ;;
  podman)
    echo "Enabling podman.socket for the current user..."
    systemctl --user enable --now podman.socket
    SOCK="/run/user/$(id -u)/podman/podman.sock"
    echo "Socket should be at: $SOCK"
    if [ -S "$SOCK" ]; then
      echo "Export this in your shell to use podman as Docker socket:"
      echo "  export DOCKER_HOST=unix://$SOCK"
    else
      echo "Warning: podman socket not found. Check 'systemctl --user status podman.socket'"
    fi
    ;;
  compose)
    echo "Running: docker-compose up --build"
    docker-compose up --build
    ;;
  *)
    usage
    exit 2
    ;;
esac

exit 0
