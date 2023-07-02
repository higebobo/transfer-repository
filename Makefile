MAKEFLAGS += --warn-undefined-variables
SHELL := /bin/bash
.SHELLFLAGS := -eu -o pipefail -c
.DEFAULT_GOAL := run

# all targets are phony
.PHONY: $(shell egrep -o ^[a-zA-Z_-]+: $(MAKEFILE_LIST) | sed 's/://')

GITHUB_ACCOUNT=john
GITHUB_TOKEN=xxx

# .env
ifneq ("$(wildcard ./.env)","")
  include ./.env
endif

run: ## Run main program
	@python main.py

run-github-jpec: ## Get github jpec-website
	@python main.py github jpec

run-github-toyoake: ## Get github toyoakekaki
	@python main.py github toyoake

run-gitlab: ## Get gitlab
	@python main.py gitlab

run-bitbucket: ## Get bitbucket
	@python main.py bitbucket

clean: ## Clear working directory
	@rm -fr work/*

help: ## Print this help
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z0-9_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)
