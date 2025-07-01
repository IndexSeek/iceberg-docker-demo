# list justfile recipes
default:
    just --list

# install dependencies
sync:
    uv sync

# setup development environment
setup:
    #!/usr/bin/env bash
    set -euo pipefail

    echo "Setting up iceberg-docker-demo..."
    uv sync
    docker-compose up -d
    echo "Setup complete!"

# start all services
up *services:
    #!/usr/bin/env bash
    set -euo pipefail

    if [ -n "$CI" ]; then
        args=(--quiet-pull --no-color)
    else
        args=()
    fi

    docker-compose up --build --wait "${args[@]}" {{ services }}

# create PostgreSQL catalog service
create-catalog:
    #!/usr/bin/env bash
    set -euo pipefail

    echo "Starting PostgreSQL catalog service..."
    docker-compose up -d postgres
    docker-compose up catalog-init
    echo "Catalog service ready!"

# start warehouse service (Minio) and initialize S3 bucket
create-warehouse:
    #!/usr/bin/env bash
    set -euo pipefail

    echo "Starting Minio warehouse service..."
    docker-compose up -d minio
    echo "Waiting for Minio to be healthy..."
    timeout 60 bash -c 'until docker-compose ps minio | grep -q "healthy"; do sleep 2; done' || echo "Minio may still be starting up"
    echo "Initializing warehouse bucket..."
    docker-compose up minio-init
    echo "Warehouse service ready!"

# stop and remove containers; clean up networks and volumes
down *services:
    #!/usr/bin/env bash
    set -euo pipefail

    if [ -z "{{ services }}" ]; then
        docker-compose down --volumes --remove-orphans
    else
        docker-compose rm {{ services }} --force --stop --volumes
    fi

# clean untracked files and docker resources
clean:
    #!/usr/bin/env bash
    set -euo pipefail

    docker-compose down -v --remove-orphans
    docker system prune --force --volumes

# tail logs for one or more services
tail *services:
    docker-compose logs --follow {{ services }}
