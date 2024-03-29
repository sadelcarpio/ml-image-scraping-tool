.PHONY: venv venv-windows

AIRFLOW := airflow
SCRAPY := image_scraper
BEAM := beam_pipelines
LABELAPP := labelapp
AIRFLOW_COMPOSE := $(AIRFLOW)/docker-compose.yaml
SCRAPY_COMPOSE := $(SCRAPY)/docker-compose.yaml
BEAM_COMPOSE := $(BEAM)/docker-compose.yaml
LABELAPP_COMPOSE := $(LABELAPP)/docker-compose.yaml
KAFKA_COMPOSE := kafka/docker-compose.yaml
SPIDER := google_images_spider

# Run spider locally (Windows)
runspider-windows:
	cd $(SCRAPY) && powershell.exe -c "../venv/Scripts/python -m scrapy crawl $(SPIDER)"

# Run spider locally (WSL / Linux)
runspider:
	cd $(SCRAPY) && ../.venv/bin/python3 -m scrapy crawl $(SPIDER)

# Run on Docker Compose
airflow-compose-run:
	docker compose --project-name mlist -f $(AIRFLOW_COMPOSE) up -d --build

scrapy-compose-run:
	docker compose --project-name mlist -f $(SCRAPY_COMPOSE) up -d --build

kafka-run:
	docker compose --project-name mlist -f $(KAFKA_COMPOSE) up -d --build

labelapp-run:
	docker compose --project-name mlist -f $(LABELAPP_COMPOSE) up -d --build

run-no-airflow: kafka-run scrapy-compose-run labelapp-run

run: airflow-compose-run kafka-run scrapy-compose-run labelapp-run

down:
	docker compose --project-name mlist -f $(KAFKA_COMPOSE) down
	docker compose --project-name mlist -f $(SCRAPY_COMPOSE) down
	docker compose --project-name mlist -f $(AIRFLOW_COMPOSE) down
	docker compose --project-name mlist -f $(LABELAPP_COMPOSE) down

down-no-airflow:
	docker compose --project-name mlist -f $(KAFKA_COMPOSE) down
	docker compose --project-name mlist -f $(SCRAPY_COMPOSE) down
	docker compose --project-name mlist -f $(LABELAPP_COMPOSE) down

beam-run:
	docker compose -f $(BEAM_COMPOSE) up -d --build

beam-down:
	docker compose -f $(BEAM_COMPOSE) down
