.PHONY: check-github-ratelimit edx-import-github-to-json \
        edx-import-json-to-terraform edx-import-lint edx-import-requirements \
        edx-import-requirements-dev format

format:
	terraform fmt
	terraform fmt modules/repo
	terraform fmt modules/user
	terraform fmt modules/role

check-github-ratelimit:
	curl --header "Authorization: token $${GITHUB_TOKEN}" "https://api.github.com/rate_limit"

edx-import-github-to-json:
	python -m edx_import.github_to_json edx
	python -m edx_import.github_to_json edx-solutions
	# Rename edx-solutions to edxsolutions because it makes the generated
	# `edxsolutions_` Terraform blocks more distinct from the `edx_` blocks.
	cd edx_import && mv export-edx-solutions.json export-edxsolutions.json
	python -m edx_import.github_to_json openedx

edx-import-json-to-terraform:
	# Delete existing users files, because json_to_terraform.py looks at
	# them in order to avoid duplicating users between exports of different orgs.
	rm users_openedx.tf users_edx.tf users_edxsolutions.tf -f
	python -m edx_import.json_to_terraform openedx
	# Do 'phony' exports for edx and edxsolutions, allowing us to generate and
	# merge the Terraform for those repos without having any effect yet.
	python -m edx_import.json_to_terraform edx --phony
	python -m edx_import.json_to_terraform edxsolutions --phony
	terraform fmt

edx-import-lint:
	black edx_import
	isort edx_import
	mypy edx_import
	pylint edx_import

edx-import-requirements:
	pip install \
		"pygithub>=1.55" \
		"requests>=2.26"

edx-import-requirements-dev: edx-import-requirements
	pip install \
	 	black \
	 	isort \
	 	mypy \
	 	pylint \
	 	types-requests
