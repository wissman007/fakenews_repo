#!/bin/bash
set -e

export AIRFLOW__CORE__EXECUTOR="CeleryExecutor"
export AIRFLOW__CORE__SQL_ALCHEMY_CONN="postgresql+psycopg2://airflow:airflow@postgres:5432/airflow"
export AIRFLOW__CELERY__RESULT_BACKEND="db+postgresql://airflow:airflow@postgres:5432/airflow"
export AIRFLOW__CELERY__BROKER_URL="redis://redis:6379/0"
export AIRFLOW_ADMIN_USER="fakenewsadmin"
export AIRFLOW_ADMIN_PASSWORD="@fakenews!!!"


# Function to wait for a service to be ready
wait_for_service() {
  local host="$1"
  local port="$2"
  local service="$3"
  local timeout=${4:-30}
  
  echo "Waiting for $service at $host:$port to become available..."
  timeout=$timeout
  
  until nc -z "$host" "$port" > /dev/null 2>&1 || [ $timeout -le 0 ]; do
    echo "Waiting for $service connection ($timeout seconds remaining)..."
    sleep 1
    ((timeout--))
  done
  
  if [ $timeout -le 0 ]; then
    echo "Timeout: $service at $host:$port failed to start within allowed time"
    exit 1
  fi
  
  echo "$service is available"
}

# Get Airflow database host from the connection string
if [[ -n "$AIRFLOW__CORE__SQL_ALCHEMY_CONN" ]]; then
  DB_HOST=$(echo "$AIRFLOW__CORE__SQL_ALCHEMY_CONN" | awk -F@ '{print $2}' | awk -F: '{print $1}')
  DB_PORT=$(echo "$AIRFLOW__CORE__SQL_ALCHEMY_CONN" | awk -F: '{print $4}' | awk -F/ '{print $1}')
  
  # Wait for PostgreSQL to be ready
  wait_for_service "$DB_HOST" "${DB_PORT:-5432}" "PostgreSQL" 60
fi

# Get Redis host from Celery broker URL
if [[ -n "$AIRFLOW__CELERY__BROKER_URL" ]]; then
  REDIS_HOST=$(echo "$AIRFLOW__CELERY__BROKER_URL" | awk -F@ '{print $2}' | awk -F: '{print $1}')
  if [[ -z "$REDIS_HOST" ]]; then
    # Try alternate format with no auth
    REDIS_HOST=$(echo "$AIRFLOW__CELERY__BROKER_URL" | awk -F/ '{print $3}' | awk -F: '{print $1}')
  fi
  REDIS_PORT=$(echo "$AIRFLOW__CELERY__BROKER_URL" | awk -F: '{print $NF}' | awk -F/ '{print $1}')
  
  # Wait for Redis to be ready
  if [[ -n "$REDIS_HOST" && "$REDIS_HOST" != "localhost" ]]; then
    wait_for_service "$REDIS_HOST" "${REDIS_PORT:-6379}" "Redis" 30
  fi
fi

# Initialize the Airflow database if needed
if [[ "$1" == "webserver" || "$1" == "scheduler" ]]; then
  echo "Initializing Airflow database if needed..."
  airflow db init
  # airflow db check || airflow db init
  
  # Create admin user if it doesn't exist
  if [[ -n "$AIRFLOW_ADMIN_USER" && -n "$AIRFLOW_ADMIN_PASSWORD" ]]; then
    echo "Checking if Airflow admin user exists..."
    airflow users list | grep -q "$AIRFLOW_ADMIN_USER" || \
      airflow users create \
        --username "$AIRFLOW_ADMIN_USER" \
        --password "$AIRFLOW_ADMIN_PASSWORD" \
        --firstname Admin \
        --lastname User \
        --role Admin \
        --email admin@example.com
  fi
fi

# Upgrade the database schema if needed
if [[ "$1" == "webserver" || "$1" == "scheduler" ]]; then
  echo "Upgrading Airflow database schema if needed..."
  airflow db upgrade
fi

# Start the specified Airflow component
case "$1" in
  webserver)
    echo "Starting Airflow Webserver..."
    exec airflow webserver
    ;;
  scheduler)
    echo "Starting Airflow Scheduler..."
    exec airflow scheduler
    ;;
  worker)
    echo "Starting Airflow Celery Worker..."
    exec airflow celery worker
    ;;
  flower)
    echo "Starting Airflow Flower..."
    exec airflow celery flower
    ;;
  *)
    # If a custom command is provided, execute it
    echo "Executing custom command: $@"
    exec "$@"
    ;;
esac