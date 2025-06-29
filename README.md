# Iceberg Docker Demo

Docker-based local development setup for Apache Iceberg with PostgreSQL catalog and S3 warehouse.

## Setup

```bash
just setup
```

## Usage

```bash
# Launch notebook
just notebook

# Run demo
python main.py
```

## Commands

```bash
just sync               # Install dependencies
just up [service]       # Start services
just down [service]     # Stop services
just create-catalog     # Initialize PostgreSQL catalog
just create-warehouse   # Initialize S3 warehouse
just clean              # Clean up Docker resources
just tail [service]     # View logs
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
