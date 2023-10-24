AIRFLOW_COMPOSE := airflow/docker-compose.yaml
SCRAPYD_COMPOSE := image_scraper/docker-compose.yaml

airflow-run:
	docker compose -f $(AIRFLOW_COMPOSE) up -d

scrapyd-run:
	docker compose -f $(SCRAPYD_COMPOSE) up -d

run: airflow-run scrapyd-run

down:
	docker compose -f $(SCRAPYD_COMPOSE) down
	docker compose -f $(AIRFLOW_COMPOSE) down
