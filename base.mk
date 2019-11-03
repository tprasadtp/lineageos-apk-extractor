# Set the shell
SHELL := /bin/bash

# Enable Buidkit if not already set
DOCKER_BUILDKIT ?= 1

# Docker Registry
REGISTRY ?= docker.io

# Set an output prefix, which is the local directory if not specified
PREFIX?=$(shell pwd)

# Versioning shit to avoid package collisions
VERSION := $(shell git tag -l --points-at HEAD)
BRANCH := $(shell  git rev-parse --abbrev-ref HEAD)
ifeq ( $(BRANCH), "master")
	BRANCH = "latest"
endif

# Handy help menu
.PHONY: help
help: ## This help dialog.
	@IFS=$$'\n' ; \
    help_lines=(`fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##/:/'`); \
    printf "%-30s %s\n" "--------" "------------" ; \
	printf "%-30s %s\n" " Target " "    Help " ; \
    printf "%-30s %s\n" "--------" "------------" ; \
    for help_line in $${help_lines[@]}; do \
        IFS=$$':' ; \
        help_split=($$help_line) ; \
        help_command=`echo $${help_split[0]} | sed -e 's/^ *//' -e 's/ *$$//'` ; \
        help_info=`echo $${help_split[2]} | sed -e 's/^ *//' -e 's/ *$$//'` ; \
        printf '\033[92m'; \
        printf "%-30s %s" $$help_command ; \
        printf '\033[0m'; \
        printf "%s\n" $$help_info; \
    done

DOCKER_USER := tprasadtp
.PHONY: docker
docker: ## Create the docker image from the Dockerfile.
	@echo -e "\033[92m+ $@ \033[0m"
	@DOCKER_BUILDKIT=$(DOCKER_BUILDKIT) docker build -t $(DOCKER_USER)/$(NAME) .
	@if ! [ -z $(VERSION) ]; then \
		echo -e "\e[92mCommit is Tagggd with :: $(VERSION)\e[39m"; \
		docker tag $(DOCKER_USER)/$(NAME) $(DOCKER_USER)/$(NAME):$(VERSION); \
	elif [ $(BRANCH) == "master" ]; then \
		echo -e "\e[92mNot a tagged commit, but on master add latest.\e[39m"; \
		docker tag $(DOCKER_USER)/$(NAME) $(DOCKER_USER)/$(NAME):latest; \
	else \
		echo -e "\e[92mNot a tagged commit, not on master add tag $(BRANCH).\e[39m"; \
		docker tag $(DOCKER_USER)/$(NAME) $(DOCKER_USER)/$(NAME):$(BRANCH); \
	fi

.PHONY: docker-lint
docker-lint: Dockerfile ## Lint Dockerfile
	@echo -e "\033[92m+ $@ \033[0m"
	@echo -e "\033[34m Checking Dockerfile ...\033[0m"
	@docker run --rm -i \
		hadolint/hadolint:latest-debian \
		hadolint \
		--ignore DL3003 \
  		--ignore DL3008 \
  		--ignore SC1010 - < Dockerfile

# Python Stuff
.PHONY: requirements
requirements: ## Generate requirements.txt
	@echo -e "\033[92m+ $@ \033[0m"
	@echo -e "\033[34m Generating requirements file...\033[0m"
	@pip-compile requirements.in -q
	@echo -e "\033[34m Generating requirements-dev file...\033[0m"
	@pip-compile requirements-dev.in -q

.PHONY: requirements-sync
requirements-sync: ## Install pip deps including dev deps via pip-sync
	@echo -e "\033[92m+ $@ \033[0m"
	@echo -e "\033[34m Installing requirements{dev}.txt file...\033[0m"
	@pip-sync requirements.txt requirements-dev.txt

.PHONY: install
install: ## Install packages. Activate virtual env first!!
	@echo "+ $@"
	@pip install -r requirements.txt

.PHONY: install-dev
install-dev: ## Install dev packages. Activate virtual env first!!
	@echo "+ $@"
	@pip install -r requirements-dev.txt

.PHONY: install-all
install-all: install install-dev ## Install dev and dependency packages. Activate virtual env first!!

.PHONY: black
black: ## Black formatter
	@echo -e "\033[92m+ $@ \033[0m"
	@echo -e "\033[34m Black Formatting utils...\033[0m"
	@black --exclude vendor $(CURDIR)

.PHONY: black-lint
black-lint: ## Lint with Black
	@echo -e "\033[92m+ $@ \033[0m"
	@echo -e "\033[34m Linting utils...\033[0m"
	@black --check --exclude vendor $(CURDIR)

.PHONY: safety-check
safety-check: ## Check Package safety
	@echo -e "\033[92m+ $@ \033[0m"
	@echo -e "\033[34m Checking Environemnt...\033[0m"
	@safety check --bare
	@echo -e "\033[34m Checking Requirements...\033[0m"
	@safety check -r requirements.txt --bare
	@echo -e "\033[34m Checking Dev Requirements...\033[0m"
	@safety check -r requirements.txt --bare

.PHONY: flake8
flake8: ## Run flake8
	@echo -e "\033[92m+ $@ \033[0m"
	@echo -e "\033[34m Running flake8...\033[0m"
	@flake8

.PHONY: isort
isort: ## Run isort on all files
	@echo -e "\033[92m+ $@ \033[0m"
	@echo -e "\033[34m Running isort...\033[0m"
	@isort --recursive --atomic .

.PHONY: isort-lint
isort-lint: ## Check isort on all files
	@echo -e "\033[92m+ $@ \033[0m"
	@echo -e "\033[34m Running isort...\033[0m"
	@isort --recursive --check-only .

.PHONY: fmt
fmt: black isort ## Formatting using black  and isort (in that order)

.PHONY: lint
lint: black-lint isort-lint flake8 safety-check docker-lint ## Lint using black, isort flake8 mypy and safety and dockerfile (in that order)
