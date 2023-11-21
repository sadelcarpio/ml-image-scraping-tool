.PHONY: venv venv-windows

AIRFLOW := airflow
SCRAPY := image_scraper
BEAM := beam_pipelines
AIRFLOW_COMPOSE := $(AIRFLOW)/docker-compose.yaml
SCRAPY_COMPOSE := $(SCRAPY)/docker-compose.yaml
BEAM_COMPOSE := $(BEAM)/docker-compose.yaml
SPIDER := google_images_spider

# Setup for windows
ifeq ($(wildcard venv/.*),)
venv-windows:
	powershell.exe -c "python -m venv venv"
endif

scrapy-devenv-windows:
	powershell.exe -c "venv/Scripts/pip install -r $(SCRAPY)/requirements.txt"

airflow-devenv-windows:  # should have a requirements file on airflow folder
	powershell.exe -c "venv/Scripts/pip install apache-airflow"

devenv-windows: venv-windows scrapy-devenv-windows airflow-devenv-windows

# Setup for WSL / Linux
ifeq ($(wildcard .venv/*),)
venv:
	python3 -m venv .venv
endif

scrapy-devenv:
	. .venv/bin/activate && pip install -r $(SCRAPY)/requirements.txt

airflow-devenv:  # should have a requirements file on airflow folder
	. .venv/bin/activate && pip install apache-airflow

devenv: venv scrapy-devenv airflow-devenv

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

run: airflow-compose-run scrapy-compose-run

down:
	docker compose --project-name mlist -f $(SCRAPY_COMPOSE) down
	docker compose --project-name mlist -f $(AIRFLOW_COMPOSE) down

beam-run:
	docker compose -f $(BEAM_COMPOSE) up --build
	docker compose -f $(BEAM_COMPOSE) down
