#!/bin/bash

cd $(pwd) || exit

if docker ps --format "{{.Names}}" | grep chapter-backend; then
  echo "found a docker"
  TEST_CONTAINER_ENV=$(docker ps --format "{{.Names}}" | grep chapter-backend)
  echo "]${TEST_CONTAINER_ENV}["
else
  TEST_CONTAINER_ENV=""
  echo "not found a docker"
fi

if [[ -z "${TEST_CONTAINER_ENV}" ]]; then
  TEST_CONTAINER="nhsf_backend-local"
else
  TEST_CONTAINER="${TEST_CONTAINER_ENV}"
fi

if [[ -z "${TEST_CONTAINER_ENV}" ]]; then
  docker-compose down

  # Step 1: Docker Compose Up
  docker-compose up -d
else
  docker exec "$TEST_CONTAINER" isort --profile black .
  docker exec "$TEST_CONTAINER" black .
  docker exec "$TEST_CONTAINER" ruff check . --fix 
fi

# Step 2: Migrate the database
docker exec -it "$TEST_CONTAINER" sh -c 'PYTHONPATH=. alembic upgrade head'

# Step 3: Run pytest with coverage
docker exec -it "$TEST_CONTAINER" sh -c 'pytest --cov=. --cov-report=xml'

# Step 4: Copy coverage report back to local machine
docker cp "$TEST_CONTAINER":/app/coverage.xml ./coverage.xml
docker cp "$TEST_CONTAINER":/app/.coverage ./.coverage

# Get the current working directory

current_dir=$(pwd)

# Update the source tag in the XML file
perl -i -pe "s#<source>/app</source>#<source>${current_dir}</source>#" "coverage.xml"

if [[ -z "${TEST_CONTAINER_ENV}" ]]; then
  # Step 5: Cleanup - Docker Compose Down
  docker-compose down
fi




