.PHONY: help
help: ## Show all available tasks
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_\-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS=":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'


.PHONY: update-env
update-env: ## Updates environment according to environment.yml
	@echo "Makefile: updating environment..."
	conda env update --name botenv --file environment.yml --prune


.PHONY: test
test: ## Run all tests
	@echo "Makefile: start testing..."
	python3 -m pytest tests/ -o log_cli=true --verbose


.PHONY: test-one
test-one: ## Run one test, pass name= as parameter. Example: make test-one param=test_ai_requests
	@echo "Makefile: start testing $(name).py..."
	python3 -m pytest tests/$(name).py -o log_cli=true --verbose