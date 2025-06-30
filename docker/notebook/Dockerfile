# syntax=docker/dockerfile:1

# Use uv's official Python 3.12 slim image
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

WORKDIR /app

# Copy Python project files
COPY pyproject.toml uv.lock ./

# Install dependencies using uv with cache mount for faster builds
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-install-project --no-dev


# Copy notebooks folder and entrypoint script
COPY notebooks/ ./notebooks/
COPY docker/notebook/entrypoint.sh /entrypoint.sh

# Set PATH to include the virtual environment
ENV PATH="/app/.venv/bin:$PATH"

RUN chmod +x /entrypoint.sh

WORKDIR /app/notebooks

EXPOSE 2718

ENTRYPOINT ["/entrypoint.sh"]
