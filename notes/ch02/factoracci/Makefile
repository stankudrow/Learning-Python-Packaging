.PHONY: sync fmt lint test build bench cov

# run it in case of troubles
sync:
	uv sync --all-groups

build:
	uv build

fmt:
	uv run ruff format .

lint:
	uv run ruff format --check .
	uv run ruff check --fix .

test:
	uv run pytest

bench:
	uv run pytest \
		--benchmark-only \
		--benchmark-group-by=param:func \
		--benchmark-columns=min,mean,stddev,median \
		-m bench

cov:
	uv run pytest \
		--cov=factoracci \
		--cov-config=pyproject.toml \
		--cov-report=term-missing \
		--cov-report=html
