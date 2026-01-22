#!/usr/bin/ bash
set -e

echo "▶ Activating virtualenv"
source envs/llm/bin/activate

echo "▶ setting environment"
source .env
#export CELERY_BROKER_URL=redis://localhost:6379/0
#export CELERY_RESULT_BACKEND=redis://localhost:6379/1


echo "▶ Starting Redis (if not running)"
if ! redis-cli ping >/dev/null 2>&1; then
  redis-server --daemonize yes
fi

echo "▶ Starting Celery worker"
celery -A llm_metadata_harvester_service.core.celery_app.celery_app worker -l info &
CELERY_PID=$!

echo "▶ Starting API"
uvicorn llm_metadata_harvester_service.main:app --host 0.0.0.0 --port 8000 --reload &
API_PID=$!

trap "kill $CELERY_PID $API_PID" EXIT

wait

