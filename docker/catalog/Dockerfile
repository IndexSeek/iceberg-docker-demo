# syntax=docker/dockerfile:1

# Use uv's official Python 3.12 slim image
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

# Set working directory
WORKDIR /app

# Copy Python project files
COPY pyproject.toml uv.lock ./

# Install dependencies using uv with cache mount for faster builds
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-install-project --no-dev

# Copy the init script
COPY docker/catalog/init-catalog.py /init-catalog.py

# Set PATH to include the virtual environment
ENV PATH="/app/.venv/bin:$PATH"

# Run the catalog initialization
CMD ["python", "/init-catalog.py"]
