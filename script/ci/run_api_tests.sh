#!/bin/bash
set -e

RESULTS_DIR="./allure-results"
REPORT_DIR="./allure-report"

mkdir -p $RESULTS_DIR

cleanup() {
    echo "🧹 Cleaning up Docker resources..."
    docker compose -f docker-compose.test.yml down -v
    echo "✅ Cleanup completed"
}

trap cleanup EXIT

echo "⚙️ Prepare environment..."
docker compose -f docker-compose.test.yml up -d

echo "⏳ Waiting for starting up services (healthchecks)..."

services=("ai-workshop-postgres-test" "ai-workshop-minio-test" "ai-workshop-redis-test" "ai-workshop-backend-test")

for service in "${services[@]}"
do
  echo "Waiting service: ${service} ..."
  for i in {1..30}; do
    status=$(docker inspect --format='{{.State.Health.Status}}' $service 2>/dev/null || echo "starting")
    if [ "$status" == "healthy" ]; then
      echo "✅ $service healthy!"
      break
    else
      echo "⏳ $service status: $status (попытка $i/30)"
      sleep 2
    fi
    if [ $i -eq 30 ]; then
      echo "❌ $service could not start up"
      docker ps -a
      echo "---- $service logs ----"
      docker logs $service
      exit 1
    fi
  done
done

echo "⚙️ Run migrations..."
export PYTHONPATH=$PWD
ENV=TEST poetry run alembic upgrade head

echo "⚙️ Run API tests..."
export PYTHONPATH=$PWD

ENV=TEST poetry run pytest tests/api --alluredir=$RESULTS_DIR -v

echo "✅ API testing is finished"
