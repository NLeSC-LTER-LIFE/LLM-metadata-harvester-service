#!/usr/bin/ bash
set -e

PID_DIR=".run"
mkdir -p "$PID_DIR"

#echo " Activating virtualenv"
#source envs/llm/bin/activate

echo " setting environment"
source .env
#export CELERY_BROKER_URL=redis://localhost:6379/0
#export CELERY_RESULT_BACKEND=redis://localhost:6379/1


echo "Starting Redis (if not running)"
if ! redis-cli ping >/dev/null 2>&1; then
  redis-server --daemonize yes
  echo "redis" > "$PID_DIR/redis.managed"
fi

echo " Starting Celery worker"
celery -A llm_metadata_harvester_service.core.celery_app.celery_app worker -l info &
echo $! > "$PID_DIR/celery.pid"

echo "Starting API"
uvicorn llm_metadata_harvester_service.main:app --host 0.0.0.0 --port 8000 --reload &
echo $! > "$PID_DIR/api.pid"

echo "Services started"

