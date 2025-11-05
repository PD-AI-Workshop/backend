#!/bin/bash

set -e

echo "⚙️ Prepare enviroment..."
docker compose -f docker-compose.test.yml up -d

echo "⏳ Waiting for starting up services (healthchecks)..."

services=("ai-workshop-postgres-test" "ai-workshop-minio-test" "ai-workshop-redis-test")

for service in "${services[@]}"
do
  echo "Waiting service: ${service} ..."
  for i in {1..30}; do
    status=$(docker inspect --format='{{.State.Health.Status}}' $service)
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
ENV=TEST alembic upgrade head

echo "⚙️ Run integration tests..."
ENV=TEST pytest \
  --cov=service \
  --cov=repository \
  --cov-report=html \
  tests/integration

echo "✅ Integration testing is finished"
docker compose -f docker-compose.test.yml down -v

