##@ Project's Makefile, with utility commands for the project development lifecycle.

MAKEFLAGS += --no-print-directory
HELP_COLUMN=11

UV=uv
PYTHON=$(UV) run python
PRE_COMMIT=$(UV) run pre-commit
COMMITIZEN=$(UV) run cz
RUFF=$(UV) run --group lint ruff
MYPY=$(UV) run --group lint mypy
TOX=$(UV) run --group test tox -qq
PYTEST=$(UV) run --group test pytest
MKDOCS=$(UV) run --group docs --directory docs mkdocs

.PHONY: default pipeline setup install install-dev release pre-commit
.PHONY: shell build lint lint-watch test test-matrix docs docs-live clean help

default: help

pipeline: clean build lint test-matrix docs ## Run clean, build, lint, test-matrix, docs.

setup: install-dev ## Run 'install-dev' and install pre-commit hooks.
	@$(PRE_COMMIT) install --install-hooks \
		--hook-type pre-commit \
		--hook-type commit-msg \
		--hook-type pre-push

install: ## Install in the python venv.
	@$(UV) sync --no-dev --no-editable --all-extras

install-dev: ## Install in editable mode inside the python venv with all extras and dev dependencies.
	@$(UV) sync --all-extras --inexact

release: ## Bump version, create tag and update 'CHANGELOG.md'.
	@$(COMMITIZEN) bump --yes --changelog
	@./scripts/update_latest_tag_msg.sh

pre-commit: ## Run all pre-commit hooks.
	@$(PRE_COMMIT) run --all-files
	@$(PRE_COMMIT) run --all-files --hook-stage pre-push

shell: ## Open Python shell.
	@$(PYTHON)

build: ## Build wheel and tar.gz in 'dist/'.
	@$(UV) build

lint: ## Lint python source code.
	@$(RUFF) format --force-exclude --exit-non-zero-on-format src tests
	@$(RUFF) check --fix --force-exclude --exit-non-zero-on-fix src tests
	@$(MYPY) src

lint-watch: ## Watch for src Python files changes and run `make lint`.
	@$(UV) run scripts/watch.py --clear --filter "*.py" src "make lint"

test: export COVERAGE_FILE = tests-reports/py310/coverage-data
test: ## Run automated tests.
	@$(PYTEST) \
        --junit-xml=tests-reports/py310/junit-report.xml \
        --cov-report=html:tests-reports/py310/coverage-html \
        --cov-report=xml:tests-reports/py310/coverage.xml \
        --html=tests-reports/py310/index.html \
        --self-contained-html

test-matrix: ## Run automated tests across multiple isolated python versions.
	@$(TOX)

docs: ## Build the documentation.
	@$(MKDOCS) build

docs-live: ## Live-edition of the documentation.
	@$(MKDOCS) serve

clean: ## Clean temporary files, like python '__pycache__', dist build, docs output, tests reports.
	@find src tests -regex "^.*\(__pycache__\|\.py[co]\)$$" -delete
	@rm -rf dist .coverage tests-reports docs/build .*_cache

help: ## Show this help.
	@printf "\033[1m################\n#     Help     #\n################\033[0m\n"
	@awk 'BEGIN {FS = ":.*##@"; printf "\n"} /^##@/ { printf "%s\n", substr($$0, 5) } ' $(MAKEFILE_LIST)
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n\n  make \033[36m<target>\033[0m\n\n"} /^[$$()% a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-$(HELP_COLUMN)s\033[0m %s\n", $$1, $$2 } ' $(MAKEFILE_LIST)
	@printf "\n"
