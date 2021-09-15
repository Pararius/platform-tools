help: ## Show this help message.
	@echo 'usage: make [target] ...'
	@echo
	@echo 'targets:'
	@egrep '^(.+)\:(.+)?\ ##\ (.+)' ${MAKEFILE_LIST} | column -t -c 2 -s ':#'

cs: ## Checks for code style issues
	docker-compose run --rm python black --check .

cs-fix: ## Fixes code style issues
	docker-compose run --rm python black .
