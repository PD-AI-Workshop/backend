#!/bin/bash



echo "⚙️ Prepare enviroment..."
docker compose -f docker-compose.test.yml up -d minio-test

service="ai-workshop-minio-test"

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

echo "⚙️ Start unit testing..."
export PYTHONPATH=$PWD
ENV=TEST poetry run pytest --cov=service --cov-report=html tests/unit

echo "✅ Unit testing finished"
docker compose -f docker-compose.test.yml down minio-test -v