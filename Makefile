.PHONY: check-github-ratelimit format migrate-github-to-json \
        migrate-json-to-terraform migrate-lint migrate-requirements \
        migrate-requirements-dev

format:
	terraform fmt
	terraform fmt modules/repo
	terraform fmt modules/user
	terraform fmt modules/role

check-github-ratelimit:
	curl --header "Authorization: token $${GITHUB_TOKEN}" "https://api.github.com/rate_limit"

migrate-github-to-json:
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

migrate-lint:
	black migrate
	isort migrate
	mypy migrate
	pylint migrate

migrate-requirements:
	pip install -r requirements.txt

migrate-requirements-dev: migrate-requirements
	pip install -r dev-requirements.txt
