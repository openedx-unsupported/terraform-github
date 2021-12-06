.PHONY: check-github-ratelimit format migrate-github-to-json \
        migrate-json-to-terraform migrate-lint migrate-requirements \
        migrate-requirements-dev

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

migrate-github-to-json: ## export edx and edx-solutions github org data to JSON
	python -m migrate.github_to_json edx
	python -m migrate.github_to_json edx-solutions
	# Rename edx-solutions to edxsolutions because it makes the generated
	# `edxsolutions_` Terraform blocks more distinct from the `edx_` blocks.
	cd migrate && mv export-edx-solutions.json export-edxsolutions.json
	python -m migrate.github_to_json openedx

migrate-json-to-terraform:
	# Delete existing users files, because json_to_terraform.py looks at
	# them in order to avoid duplicating users between exports of different orgs.
	rm users_openedx.tf users_edx.tf users_edxsolutions.tf -f
	python -m migrate.json_to_terraform openedx
	# Do 'phony' exports for edx and edxsolutions, allowing us to generate and
	# merge the Terraform for those repos without having any effect yet.
	python -m migrate.json_to_terraform edx --phony
	python -m migrate.json_to_terraform edxsolutions --phony
	terraform fmt

migrate-lint: ## Lint and format migration related python scripts.
	black migrate
	isort migrate
	mypy migrate
	pylint migrate

migrate-requirements: ## Install requirements needed to run migration scripts.
	pip install -r requirements.txt

migrate-requirements-dev: migrate-requirements ## Install dev requirements for migration scripts.
	pip install -r dev-requirements.txt
