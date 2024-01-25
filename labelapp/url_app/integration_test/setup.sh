#!/bin/bash

# Setup Kafka broker
docker compose --project-name integration-test -f ../../kafka/docker-compose.yaml up -d
docker run -d --name labelapp-postgres --network integration-test_default --env-file ../.env postgres:latest
docker build . -t url-app
docker run -d --name url-app --network integration-test_default --env-file ../.env url-app

sleep 5

# Run container to produce messages and populate db
docker build . -t url-app-test
docker run --rm --network integration-test_default --env-file ../.env -v \
"${PWD}"/integration_test:/url_app/integration_test url-app-test python -m integration_test.produce_kafka_messages

sleep 5

# Cleanup containers
docker compose --project-name integration-test -f ../../kafka/docker-compose.yaml down
docker stop labelapp-postgres
docker stop url-app
docker rm labelapp-postgres
docker rm url-app
