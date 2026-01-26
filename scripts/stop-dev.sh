#!/usr/bin/bash
set -e

PID_DIR=".run"

echo "Stopping services"

stop_pid() {
  local name="$1"
  local pid_file="$PID_DIR/$2"

  if [[ -f "$pid_file" ]]; then
    pid=$(cat "$pid_file")
    if kill -0 "$pid" 2>/dev/null; then
      echo "▶ Stopping $name (PID $pid)"
      kill "$pid"
      sleep 2

      if kill -0 "$pid" 2>/dev/null; then
        echo "!! $name did not stop gracefully, killing"
        kill -9 "$pid"
      fi
    fi
    rm -f "$pid_file"
  else
    echo " info:  $name not running"
  fi
}

stop_pid "API" "api.pid"
stop_pid "Celery worker" "celery.pid"

if [[ -f "$PID_DIR/redis.managed" ]]; then
  echo "Stopping Redis"
  redis-cli shutdown || true
  rm -f "$PID_DIR/redis.managed"
fi

echo "Cleanup"
rmdir "$PID_DIR" 2>/dev/null || true

echo "All services stopped"