# Primary Targets

.PHONY: all build test

all: build test

GO_SERVICES := $(shell find . -name 'go.mod' -not -path '*/vendor/*' -exec dirname {} \; | sort -u)
PYTHON_SERVICES := $(shell find . -name 'tox.ini' -not -path '*/.venv/*' -exec dirname {} \; | sort -u)

BUILD_TARGETS := $(GO_SERVICES)

build: $(BUILD_TARGETS)

test: test-unit

# Testing

.PHONY: test-unit test-unit-go test-unit-python

test-unit: test-unit-go test-unit-python

test-unit-go:
	@for service in $(GO_SERVICES); do \
		echo "==> go test: $$service"; \
		(cd $$service && go test ./...) || exit 1; \
	done

test-unit-python:
	@for service in $(PYTHON_SERVICES); do \
		echo "==> tox tests: $$service"; \
		(cd $$service && tox -e tests) || exit 1; \
	done

# Linting and formatting

.PHONY: lint lint-go lint-python format

lint: lint-go lint-python

lint-go:
	@for service in $(GO_SERVICES); do \
		echo "==> golangci-lint: $$service"; \
		(cd $$service && golangci-lint run --fix --timeout=5m) || exit 1; \
	done

lint-python:
	@for service in $(PYTHON_SERVICES); do \
		echo "==> tox pre-commit: $$service"; \
		(cd $$service && tox -e pre-commit) || exit 1; \
	done

# Help

help:
	@echo "Available targets:"
	@echo "  test-unit: Run unit tests"
