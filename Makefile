.PHONY: check-github-ratelimit format help migrate-github-to-json migrate-lint \
        migrate-requirements migrate-requirements-dev

help: ## display this help message
	@echo "Please use \`make <target>' where <target> is one of"
	@grep '^[a-zA-Z]' $(MAKEFILE_LIST) | sort | awk -F ':.*?## ' 'NF==2 {printf "\033[36m  %-25s\033[0m %s\n", $$1, $$2}'

format:  ## Format all the terraform files
	terraform fmt
	terraform fmt modules/repo
	terraform fmt modules/user
	terraform fmt modules/role

check-github-ratelimit: ## Check your github rate limits
	curl --header "Authorization: token $${GITHUB_TOKEN}" "https://api.github.com/rate_limit"

migrate-github-to-json: ## export openedx github org data
	python -m migrate.github_to_json openedx

migrate-lint: ## Lint and format migration related python scripts.
	black migrate
	isort migrate
	mypy migrate
	pylint migrate

migrate-requirements: ## Install requirements needed to run migration scripts.
	pip install -r requirements.txt

migrate-requirements-dev: migrate-requirements ## Install dev requirements for migration scripts.
	pip install -r dev-requirements.txt
