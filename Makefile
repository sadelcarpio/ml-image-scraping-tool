.PHONY: venv venv-windows

AIRFLOW := airflow
SCRAPY := image_scraper
AIRFLOW_COMPOSE := $(AIRFLOW)/docker-compose.yaml
SCRAPY_COMPOSE := $(SCRAPY)/docker-compose.yaml
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
	cd $(SCRAPY) && powershell.exe -c "../venv/Scripts/scrapy crawl $(SPIDER)"

# Run spider locally (WSL / Linux)
runspider:
	cd $(SCRAPY) && source ../.venv/bin/scrapy crawl $(SPIDER)

# Run on Docker Compose
airflow-compose-run:
	docker compose -f $(AIRFLOW_COMPOSE) up -d

scrapy-compose-run:
	docker compose -f $(SCRAPY_COMPOSE) up -d

run: airflow-compose-run scrapy-compose-run

down:
	docker compose -f $(SCRAPY_COMPOSE) down
	docker compose -f $(AIRFLOW_COMPOSE) down
