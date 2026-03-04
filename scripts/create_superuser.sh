#!/usr/bin/env bash
set -euo pipefail

HELPER_NAME="create_superuser.sh"

usage() {
  cat <<EOF
Usage: $HELPER_NAME [--username USER] [--email EMAIL] [--password PASS] [--interactive]

Options:
  --username USER    Username for the superuser (default: admin)
  --email EMAIL      Email for the superuser (default: admin@example.com)
  --password PASS    Password for the superuser (if omitted, runs interactive createsuperuser)
  --interactive      Force interactive `createsuperuser` (useful for prompts)

Examples:
  # Interactive (inside container if running):
  ./scripts/create_superuser.sh --interactive

  # Non-interactive (create with provided credentials):
  ./scripts/create_superuser.sh --username admin --email you@example.com --password secret
EOF
}

USERNAME="admin"
EMAIL="rfanomezaniavo@gmail.com"
PASSWORD="admin"
INTERACTIVE=0

# Paths used for manage.py in container vs local
CONTAINER_MANAGE_PY_DIR="/app/code/pointageProject"
LOCAL_MANAGE_PY="./django/code/pointageProject/manage.py"

while [ "$#" -gt 0 ]; do
  case "$1" in
    --username) USERNAME="$2"; shift 2;;
    --email) EMAIL="$2"; shift 2;;
    --password) PASSWORD="$2"; shift 2;;
    --interactive) INTERACTIVE=1; shift;;
    -h|--help) usage; exit 0;;
    *) echo "Unknown arg: $1"; usage; exit 2;;
  esac
done

PY_SNIPPET="from django.contrib.auth import get_user_model\nUser=get_user_model()\nif not User.objects.filter(username='${USERNAME}').exists():\n    User.objects.create_superuser('${USERNAME}','${EMAIL}','${PASSWORD}')\n    print('Superuser created')\nelse:\n    print('Superuser already exists')\n"

run_in_container() {
  # Decide whether to run inside the django container or locally
  if command -v docker-compose >/dev/null 2>&1 && docker-compose ps django >/dev/null 2>&1; then
    # run inside the django service; ensure working dir points to the project
    CONTAINER_CMD=(docker-compose exec -T -w /app/code django bash -lc)
    IN_CONTAINER=1
  else
    CONTAINER_CMD=(bash -lc)
    IN_CONTAINER=0
  fi

  if [ "$INTERACTIVE" -eq 1 ]; then
    echo "Running interactive creation inside $( [ $IN_CONTAINER -eq 1 ] && echo container || echo local )..."
    if [ "$IN_CONTAINER" -eq 1 ]; then
      "${CONTAINER_CMD[@]}" "python ${CONTAINER_MANAGE_PY_DIR#/app/code/}/manage.py createsuperuser"
    else
      "${CONTAINER_CMD[@]}" "python ${LOCAL_MANAGE_PY} createsuperuser"
    fi
    return
  fi

  if [ -n "${PASSWORD:-}" ]; then
    echo "Creating non-interactive superuser: $USERNAME ($EMAIL)"
    # Pipe the Python snippet into manage.py shell to avoid here-doc quoting issues
    if [ "$IN_CONTAINER" -eq 1 ]; then
      # In-container: working dir is /app/code, run pointageProject/manage.py
      "${CONTAINER_CMD[@]}" "printf '%s\n' \"${PY_SNIPPET}\" | python pointageProject/manage.py shell"
    else
      "${CONTAINER_CMD[@]}" "printf '%s\n' \"${PY_SNIPPET}\" | python ${LOCAL_MANAGE_PY} shell"
    fi
  else
    echo "Password not provided — running interactive createsuperuser"
    if [ "$IN_CONTAINER" -eq 1 ]; then
      "${CONTAINER_CMD[@]}" "python pointageProject/manage.py createsuperuser"
    else
      "${CONTAINER_CMD[@]}" "python ${LOCAL_MANAGE_PY} createsuperuser"
    fi
  fi
}

run_in_container
