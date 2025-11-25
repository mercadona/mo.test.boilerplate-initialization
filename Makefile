#!/usr/bin/make -f

.DEFAULT_GOAL := help

.PHONY: install-test-requirements test linting build
.PHONY: env-start env-stop env-recreate docker-cleanup bash shell 
.PHONY: pr changelog prepare-deploy view-logs

ROOT_FOLDER := $(shell pwd)
DOCKER_COMPOSE_FILE := $(ROOT_FOLDER)/docker/docker-compose.yml
DOCKER_COMPOSE_OVERRIDE_FILE := $(ROOT_FOLDER)/docker/docker-compose-extra.yml
PROJECT_NAME := jabberwocky

DOCKER_COMMAND := docker compose -p $(PROJECT_NAME) -f $(DOCKER_COMPOSE_FILE)
ifneq ("$(wildcard $(DOCKER_COMPOSE_OVERRIDE_FILE))","")
DOCKER_COMMAND := $(DOCKER_COMMAND) -f $(DOCKER_COMPOSE_OVERRIDE_FILE)
endif

install-test-requirements: ## Install all test dependencies
	$(DOCKER_COMMAND) exec -T app pip install --disable-pip-version-check -r /app/requirements/test.txt

install-lint-requirements: ## Install all linting dependencies
	$(DOCKER_COMMAND) exec -T app pip install --disable-pip-version-check -r /app/requirements/linting.txt

install-ci-requirements: install-test-requirements install-lint-requirements  ## Install all CI dependencies

test: ## Run test suite in project's main container
	$(DOCKER_COMMAND) exec -T app pytest

linting: check-types check-style check-format ## Check/Enforce Python Code-Style

check-types: ## Run mypy
	$(DOCKER_COMMAND) exec -T app mypy .

check-style: ## Run ruff check
	$(DOCKER_COMMAND) exec -T app ruff check .

check-format: ## Run ruff format
	$(DOCKER_COMMAND) exec -T app ruff format --check .

fix-linting: fix-format fix-style ## Makes Python Linting happy

fix-style: ## Fix style with ruff
	$(DOCKER_COMMAND) exec -T app ruff check --fix .

fix-format: ## Fix format with ruff
	$(DOCKER_COMMAND) exec -T app ruff format .

build: ## Build project image
	$(DOCKER_COMMAND) build --no-cache --pull

env-start: ## Start project containers defined in docker-compose
	$(DOCKER_COMMAND) up -d

env-stop: ## Stop project containers defined in docker-compose
	$(DOCKER_COMMAND) stop

env-restart: env-stop env-start ## Restart project containers defined in docker-compose

env-destroy: ## Destroy all project containers
	$(DOCKER_COMMAND) down -v --rmi all --remove-orphans

env-recreate: build env-start install-test-requirements ## Force building project image and start all containers again

env-reset: destroy-containers env-start install-test-requirements ## Destroy project containers and start them again

destroy-containers: ## Destroy project containers
	$(DOCKER_COMMAND) down -v

docker-cleanup: ## Purge all Docker images in the system
	$(DOCKER_COMMAND) down -v
	docker system prune -f

migrations: ## Creates new alembic revision
	$(DOCKER_COMMAND) exec app alembic revision --autogenerate

migrate: ## Creates new alembic revision
	$(DOCKER_COMMAND) exec app alembic upgrade head

bash: ## Open a bash shell in project's main container
	$(DOCKER_COMMAND) exec app bash

shell: ## Open a Django shell in project's main container
	$(DOCKER_COMMAND) exec app python -i app.py

pr: ## Push and open github pull request page
	@create_pull_request

changelog: ## Generate changelog for current release
	@PROJECT_NAME=$(PROJECT_NAME) git_generate_changelog

prepare-deploy: ## Create tag for next release, generate changelog and open tag on jenkins
	@PROJECT_NAME=$(PROJECT_NAME) mercadona_prepare_deploy

view-logs: ## Show logs
	$(DOCKER_COMMAND) logs -f

help: ## Display this help text
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
