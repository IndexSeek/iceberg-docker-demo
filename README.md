# Iceberg Docker Demo

Docker-based local development setup for Apache Iceberg with PostgreSQL catalog and S3 warehouse.

## Setup

```bash
just setup
```

This will install Python dependencies, start all Docker services, and automatically initialize the Iceberg catalog.

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

Once services are running, the Iceberg catalog with default namespace is automatically initialized. You can verify the setup by checking the service logs:

```bash
just tail catalog-init
```

## Services

- **PostgreSQL** (port 5432): Iceberg catalog metadata
- **LocalStack** (port 4566): S3-compatible storage
- **catalog-init**: Initializes Iceberg catalog with default namespace
- **localstack-init**: Creates S3 warehouse bucket

## Environment Variables

The setup supports customization via environment variables:

### Database Configuration
- `POSTGRES_USER` (default: postgres)
- `POSTGRES_PASSWORD` (default: postgres)
- `POSTGRES_DB` (default: iceberg_catalog)

### S3/Object Storage Configuration
- `S3_ENDPOINT` (default: http://localstack:4566)
- `S3_ACCESS_KEY_ID` (default: test)
- `S3_SECRET_ACCESS_KEY` (default: test)
- `WAREHOUSE_PATH` (default: s3://warehouse/)

### AWS CLI Configuration
- `AWS_ACCESS_KEY_ID` (default: test)
- `AWS_SECRET_ACCESS_KEY` (default: test)
- `AWS_DEFAULT_REGION` (default: us-east-1)
- `AWS_ENDPOINT_URL` (default: http://localstack:4566)

## Requirements

- Docker & Docker Compose
- Python 3.10+
- [uv](https://github.com/astral-sh/uv)
- [just](https://github.com/casey/just)

## Trademarks

Apache Iceberg, Iceberg, Apache, the Apache feather logo, and the Apache Iceberg project logo are either registered trademarks or trademarks of The Apache Software Foundation.
