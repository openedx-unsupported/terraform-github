.PHONY: edx_import_do_export edx_import_install edx_import_install_dev \
        edx_import_lint

edx_import_do_export:
	python -m edx_import.github_to_json 1> edx_import/export.json

edx_import_lint:
	black edx_import
	isort edx_import
	mypy edx_import
	pylint edx_import

edx_import_install:
	pip install \
	  "pygithub>=1.55" \
	  "requests>=2.26"

edx_import_install_dev: edx_import_install
	pip install \
	  black \
	  isort \
	  mypy \
	  pylint \
	  types-requests
