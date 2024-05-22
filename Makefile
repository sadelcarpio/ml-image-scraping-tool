.PHONY: venv venv-windows

AIRFLOW := airflow
SCRAPY := image_scraper
BEAM := beam_pipelines
LABELAPP := labelapp
AIRFLOW_COMPOSE := $(AIRFLOW)/docker-compose.yaml
SCRAPY_COMPOSE := $(SCRAPY)/docker-compose.yaml
LABELAPP_COMPOSE := $(LABELAPP)/docker-compose.yaml
KAFKA_COMPOSE := kafka/docker-compose.yaml
SPIDER := google_images_spider

# Run on Docker Compose
airflow-compose-run:
	docker compose --project-name mlist -f $(AIRFLOW_COMPOSE) up -d --build

scrapy-compose-run:
	docker compose --project-name mlist -f $(SCRAPY_COMPOSE) up -d --build

kafka-run:
	docker compose --project-name mlist -f $(KAFKA_COMPOSE) up -d --build

labelapp-run:
	docker compose --project-name mlist -f $(LABELAPP_COMPOSE) up -d --build

beam-build:
	docker build -f $(BEAM)/upload_csv_labels.Dockerfile -t beam-upload-csv beam_pipelines

run: airflow-compose-run kafka-run scrapy-compose-run labelapp-run beam-build

run-no-airflow: kafka-run scrapy-compose-run labelapp-run

down:
	docker compose --project-name mlist -f $(KAFKA_COMPOSE) down
	docker compose --project-name mlist -f $(SCRAPY_COMPOSE) down
	docker compose --project-name mlist -f $(AIRFLOW_COMPOSE) down
	docker compose --project-name mlist -f $(LABELAPP_COMPOSE) down

down-no-airflow:
	docker compose --project-name mlist -f $(KAFKA_COMPOSE) down
	docker compose --project-name mlist -f $(SCRAPY_COMPOSE) down
	docker compose --project-name mlist -f $(LABELAPP_COMPOSE) down

# Unit Testing
test-airflow:
	docker run --rm -v ${PWD}/$(AIRFLOW)/dags:/opt/airflow/dags -v ${PWD}/$(AIRFLOW)/tests:/opt/airflow/tests \
	apache/airflow:2.7.2 python -m unittest discover tests

test-image-scraper:
	docker build image_scraper --file $(SCRAPY)/base.Dockerfile --tag scrapyd-deploy
	docker run --rm scrapyd-deploy python -m unittest discover tests

test-url-app:
	docker build $(LABELAPP)/url_app --file $(LABELAPP)/url_app/Dockerfile --tag url-app
	docker run --rm url-app python -m unittest discover tests

test-dag-info:
	docker build $(LABELAPP)/dag_info --file $(LABELAPP)/dag_info/Dockerfile --tag dag-info
	docker run --rm dag-info python -m unittest discover tests

test-labeling-app:
	docker build $(LABELAPP)/labeling_app --file $(LABELAPP)/labeling_app/Dockerfile --tag labeling-app
	docker run --rm labeling-app python -m unittest discover tests

test-beam:
	docker build $(BEAM) --file $(BEAM)/to_tfrecord.Dockerfile --tag pipelines
	docker run --rm pipelines python -m unittest discover tests

test-all: test-airflow test-image-scraper test-url-app test-dag-info test-labeling-app test-beam

# Integration Testing
integration-test-url-app:
	cd $(LABELAPP)/url_app && ./integration_test/test.sh
