.PHONY: update-env
update-env: ## Updates environment according to environment.yml
	@echo "Makefile: updating environment..."
	conda env update --name botenv --file environment.yml --prune


.PHONY: test
test: ## Run all tests
	@echo "Makefile: start testing..."
	python3 -m pytest tests/ -o log_cli=true --verbose


.PHONY: test-one
test-one: ## Run one test, pass name as parameter
	@echo "Makefile: start testing $(name).py..."
	python3 -m pytest tests/$(name).py -o log_cli=true --verbose