#!/bin/bash


cd $(pwd) || exit

docker-compose down

# Step 1: Docker Compose Up
docker-compose up -d

# Step 2: Migrate the database
docker exec -it nhsf_backend-local sh -c 'PYTHONPATH=. alembic upgrade head'

# Step 3: Generate new migrations
docker exec -it nhsf_backend-local sh -c 'PYTHONPATH=. alembic revision --autogenerate -m "Add matches table"'



# Step 4: Docker Compose Down
docker-compose down

