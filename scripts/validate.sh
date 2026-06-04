#!/usr/bin/env bash
set -euo pipefail

echo "Running Ruff..."
ruff check .

echo "Running Mypy..."
mypy src

echo "Running Pytest..."
pytest
