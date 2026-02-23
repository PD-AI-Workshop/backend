#!/bin/bash
set -e

RESULTS_DIR="./allure-results"
REPORT_DIR="./allure-report"
HISTORY_DIR="./allure-history"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

mkdir -p $HISTORY_DIR
mkdir -p $RESULTS_DIR

SKIP_CLEANUP=false
SKIP_ALLURE=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --skip-cleanup)
            SKIP_CLEANUP=true
            shift
            ;;
        --skip-allure)
            SKIP_ALLURE=true
            shift
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

cleanup() {
    if [ "$SKIP_CLEANUP" = false ]; then
        echo "🧹 Cleaning up Docker resources..."
        docker compose -f docker-compose.test.yml down -v
        echo "✅ Cleanup completed"
    else
        echo "🚫 Cleanup skipped (--skip-cleanup flag set)"
    fi
}

run_tests() {
    echo "⚙️ Run E2E tests..."
    export PYTHONPATH=$PWD

    if [ "$SKIP_ALLURE" = false ]; then
        ENV=TEST poetry run pytest tests/api/e2e --alluredir=./allure-results
    else
        ENV=TEST poetry run pytest tests/api/e2e
    fi
}

generate_allure_report() {
    if [ "$SKIP_ALLURE" = false ]; then
        echo "📚 Preparing allure report..."
        
        if [ -d "$REPORT_DIR/history" ]; then
            echo "📚 Copying history from previous report..."
            cp -r "$REPORT_DIR/history" "$RESULTS_DIR/"
        fi

        echo "💾 Generating allure report..."
        allure generate $RESULTS_DIR -o $REPORT_DIR --clean
        
        cp -r $REPORT_DIR $HISTORY_DIR/$TIMESTAMP
        echo "✅ Allure report saved to: $HISTORY_DIR/$TIMESTAMP"
    else
        echo "🚫 Allure report generation skipped (--skip-allure flag set)"
    fi
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
export PYTHONPATH=$PWD
ENV=TEST poetry run alembic upgrade head

run_tests

generate_allure_report

echo "✅ E2E testing is finished"
