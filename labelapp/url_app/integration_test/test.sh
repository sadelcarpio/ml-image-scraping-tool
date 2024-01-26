#!/bin/bash

# Setup Kafka broker
docker compose -f ../../kafka/docker-compose.yaml up -d
docker run -d --name labelapp-postgres --network kafka_default --env-file ../.env postgres:latest

sleep 5

# Build test container
docker build . -t url-app-test
# Setup creation of user and project in db
docker run --name url-app-test --rm --network kafka_default --env-file ../.env -v \
"${PWD}"/integration_test:/url_app/integration_test url-app-test python -m integration_test.setup
# Reset kafka offsets
docker compose -f ../../kafka/docker-compose.yaml exec kafka-service \
kafka-consumer-groups --bootstrap-server localhost:9092 --group read-urls --reset-offsets --to-earliest \
--topic google-images --execute
# Execute main program
docker run -d --name url-app-test --network kafka_default --env-file ../.env url-app-test

sleep 10

# Stop main program
docker stop url-app-test
docker rm url-app-test

# Verify expected behavior
docker run --name url-app-test --rm --network kafka_default --env-file ../.env -v \
"${PWD}"/integration_test:/url_app/integration_test url-app-test python -m unittest discover integration_test

# Cleanup containers
docker compose -f ../../kafka/docker-compose.yaml down
docker stop labelapp-postgres
docker rm labelapp-postgres