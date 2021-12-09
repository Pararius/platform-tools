help: ## Show this help message.
	@echo 'usage: make [target] ...'
	@echo
	@echo 'targets:'
	@egrep '^(.+)\:(.+)?\ ##\ (.+)' ${MAKEFILE_LIST} | column -t -c 2 -s ':#'

cs: ## Checks for code style issues
	docker-compose run --rm python black --check .
	terraform -chdir=terraform fmt -check -recursive .

cs-fix: ## Fixes code style issues
	docker-compose run --rm python black .
	terraform -chdir=terraform fmt -recursive .

build: ## Builds the image including the setup.py file (run this when you've changed dependencies)
	docker-compose build python

test: ## Runs all tests for this library
	docker-compose run --rm python pytest $(ARGS)
