# SPDX-FileCopyrightText: Copyright (C) 2025-2026 Fabrício Barros Cabral
# SPDX-License-Identifier: MIT

.PHONY: install test check format dist upgrade clean

install:
	uv sync

test:
	uv run pytest

check:
	uv run ruff check .
	uv run zuban check

format:
	uv run ruff format .

upgrade:
	uv sync --upgrade

dist: check test
	uv build

clean:
	rm -rf .venv dist *.egg-info
	find . -type d -name "*.pyc" -exec rm -r {} +
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type d -name ".ruff_cache" -exec rm -r {} +
	find . -type d -name ".pytest_cache" -exec rm -r {} +
