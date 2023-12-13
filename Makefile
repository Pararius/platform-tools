help: ## Show this help message.
	@echo 'usage: make [target] ...'
	@echo
	@echo 'targets:'
	@egrep '^(.+)\:(.+)?\ ##\ (.+)' ${MAKEFILE_LIST} | column -t -c 2 -s ':#'

cs: ## Checks for code style issues
	docker compose run --rm cs black --check .
	terraform -chdir=terraform fmt -check -recursive .

cs-fix: ## Fixes code style issues
	docker compose run --rm cs black .
	terraform -chdir=terraform fmt -recursive .

run: ## Runs a cloud function from a given context, the second argument can be used to pass the request/event
	@[ -n "$(CONTEXT)" ] || { echo 'You must supply a path to the function (context) in the form of `make run CONTEXT=./src/your-function`'; exit 1; }
	CONTEXT=$(CONTEXT) docker compose run --rm cloud-function python -c "import main; main.handler($(ARGS));"

test: ## Runs all tests for this library
	docker-compose run --rm python pytest $(ARGS)
