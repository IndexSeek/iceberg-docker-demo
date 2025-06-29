# Iceberg Docker Demo

Docker-based local development setup for Apache Iceberg with PostgreSQL catalog and S3 warehouse.

## Setup

```bash
just setup
```

This will install Python dependencies and start all Docker services.

## Commands

```bash
just sync               # Install Python dependencies
just up [service]       # Start Docker services (all or specific)
just down [service]     # Stop Docker services (all or specific)
just create-catalog     # Initialize PostgreSQL catalog
just create-warehouse   # Initialize S3 warehouse
just clean              # Clean up Docker resources
just tail [service]     # View service logs
```

## Usage

Once services are running, you can interact with the Iceberg setup:

```bash
python main.py
```

## Services

- **PostgreSQL** (port 5432): Iceberg catalog metadata
- **LocalStack** (port 4566): S3-compatible storage

## Requirements

- Docker & Docker Compose
- Python 3.10+
- [uv](https://github.com/astral-sh/uv)
- [just](https://github.com/casey/just)

## Trademarks

Apache Iceberg, Iceberg, Apache, the Apache feather logo, and the Apache Iceberg project logo are either registered trademarks or trademarks of The Apache Software Foundation.
