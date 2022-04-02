#VARIABLES
## Project stuff
.DEFAULT_GOAL:=help
COMPOSE_FILE=docker-compose.yml
PROJECT_NAME=fxtrading
USER_UID = $(shell id -u)

# --------------------------

# --------------------------
.PHONY: setup keystore certs all elk monitoring tools build down stop restart rm logs


create-migrations: ## Run django makemigrations
	UID=$(USER_UID) docker-compose -f ${COMPOSE_FILE} run --rm back ./manage.py makemigrations

manage: ## Run manage.py with the argument of your choice. If you use multiple arguments use double quotes, example 'make manage "<command> --arg"'
	UID=$(USER_UID) docker-compose -f ${COMPOSE_FILE} run --rm back ./manage.py $(filter-out $@,$(MAKECMDGOALS))

migrate: ## Run django migrations
	UID=$(USER_UID) docker-compose -f ${COMPOSE_FILE} run --rm back ./manage.py migrate

loadfixtures: ## Load fixtures using django load_data
	UID=$(USER_UID) docker-compose -f ${COMPOSE_FILE} run --rm back ./manage.py loaddata articles.json

collecstatic: ## Collect django static files
	UID=$(USER_UID) docker-compose -f ${COMPOSE_FILE} run --rm back ./manage.py collectstatic --no-input

createsuperuser: ## Create superuser
	UID=$(USER_UID) docker-compose -f ${COMPOSE_FILE} run --rm back ./manage.py createsuperuser

# Shell
django: ## Shell on django
	UID=$(USER_UID) docker-compose -f ${COMPOSE_FILE} exec back bash

psql:  ## Connect to the database using psql
	UID=$(USER_UID) docker-compose -f ${COMPOSE_FILE} exec postgres psql -U aglaia



# DockerOps
up: ## Up all the containers
	UID=$(USER_UID) docker-compose -f ${COMPOSE_FILE} up -d

ps: ## Show current running containers
	UID=$(USER_UID) docker-compose -f ${COMPOSE_FILE} ps

build: ## Up and build containers (this process can be long)
	UID=$(USER_UID) docker-compose -f ${COMPOSE_FILE} up -d --build

stop: ## Stop running containers
	UID=$(USER_UID) docker-compose -f ${COMPOSE_FILE} stop $(filter-out $@,$(MAKECMDGOALS))

logs: ## If used without arguments it will show all logs of running containers, it can be use as "make logs -f <service-name>" to show logs of an especific container
	UID=$(USER_UID) docker-compose -f ${COMPOSE_FILE} logs -f $(filter-out $@,$(MAKECMDGOALS))

restart: ## Restart containers
	UID=$(USER_UID) docker-compose -f ${COMPOSE_FILE} restart $(filter-out $@,$(MAKECMDGOALS))

destroy: ## Warning: This will erase all data
	UID=$(USER_UID) docker-compose -f ${COMPOSE_FILE} down -v

pull: ## Download a newer version of the image
	UID=$(USER_UID) docker-compose -f ${COMPOSE_FILE} pull

kick-off: ## Build apps, run everything
	@make up
	@make migrate
	@make loadfixtures
	@make collecstatic
	@make up

# Help
help:           ## Show this help.
	@echo "This Makefile will help you with the most common tasks in this project."
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m (default: help)\n\nTargets:\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-12s\033[0m %s\n", $$1, $$2 }' $(MAKEFILE_LIST)


# Hack -> https://stackoverflow.com/questions/6273608/how-to-pass-argument-to-makefile-from-command-line
%:
	@:

