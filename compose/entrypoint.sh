#!/bin/sh
set -e
set -o pipefail

echo "Container type: $CONTAINER_TYPE"

wait_for_port() {
  SERVIVE_NAME="$1"
  HOST="$2"
  PORT="$3"

  echo "Waiting for $SERVIVE_NAME at $HOST:$PORT..."

  while ! nc -z "$HOST" "$PORT"; do
      sleep 1
  done

  echo "$SERVIVE_NAME is ready"
}

wait_for_db() {
  wait_for_port "Postgres" \
  "$APP_CONFIG__DB__HOST" \
  "$APP_CONFIG__DB__PORT"
}
wait_for_rabbitmq() {
  wait_for_port "RabbitMQ" \
  "$APP_CONFIG__TASKIQ__HOST" \
  "$APP_CONFIG__TASKIQ__PORT"
}

wait_for_minio() {
  wait_for_port "MinIO" \
  "$APP_CONFIG__MINIO__HOST" \
  "$APP_CONFIG__MINIO__PORT"
}

wait_for_maildev() {
  wait_for_port "Maildev" \
  "$APP_CONFIG__EMAIL__HOST" \
  "$APP_CONFIG__EMAIL__PORT"
}


export PYTHONPATH="/app/src:$PYTHONPATH"
case "$CONTAINER_TYPE" in
  api)
    wait_for_db
    wait_for_rabbitmq
    wait_for_minio
    wait_for_maildev

    echo "Running migrations..."
    alembic -c src/alembic.ini upgrade head

    echo "Starting API..."
    exec "$@"
    ;;

  worker)
    wait_for_db
    wait_for_rabbitmq
    wait_for_maildev

    echo "Starting Taskiq worker..."
    exec taskiq worker services:broker --fs-discover --tasks-pattern "**/tasks"
    ;;

  *)
    echo "Unknown CONTAINER_TYPE: $CONTAINER_TYPE"
    exec "$@"
    ;;
esac

