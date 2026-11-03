install:
	uv sync

run:
	uv run python -m agentic main.py

clean:
	rm -rf .venv
	find . -type d -name "__pycache__" -exec rm -rf {} +