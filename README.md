# Iceberg Docker Demo

Docker-based local development setup for Apache Iceberg with PostgreSQL catalog, S3-compatible object storage, and interactive Marimo notebooks for data analysis.

## Setup

```bash
just setup
```

This will install Python dependencies, start all Docker services, initialize the
Iceberg catalog, load sample NYC taxi data, and start the Marimo notebook server.

## Commands

```bash
just sync               # Install Python dependencies
just up [service]       # Start Docker services (all or specific)
just down [service]     # Stop Docker services (all or specific)
just create-catalog     # Initialize PostgreSQL catalog
just create-warehouse   # Initialize warehouse storage bucket
just clean              # Clean up Docker resources
just tail [service]     # View service logs
```

## Usage

Once services are running:

1. **Iceberg catalog** with default namespace is automatically initialized
2. **Sample NYC taxi data** is loaded into the `nyc.fhvhv` table
3. **Marimo notebook server** is available at http://localhost:2718

You can verify the setup by checking the service logs:

```bash
just tail catalog-init   # Check catalog initialization
just tail marimo        # Check notebook server status
```

## Services

- **PostgreSQL** (port 5432): Iceberg catalog metadata
- **Minio** (ports 9000/9001): S3-compatible object storage backend
- **Marimo** (port 2718): Interactive notebook server for data analysis
- **catalog-init**: Initializes Iceberg catalog with PyIceberg environment variables
- **minio-init**: Creates S3 storage bucket and uploads sample data

## Data Analysis

The setup includes a Marimo notebook (`notebooks/reading.py`) that demonstrates:
- Connecting to the Iceberg catalog using PyIceberg's `load_catalog()`
- Listing namespaces and tables
- Querying and displaying NYC taxi data
- Interactive data exploration

The project uses PyIceberg's recommended environment variable configuration with
`PYICEBERG_CATALOG__DEFAULT__*` variables for catalog settings.

Access the notebook interface at http://localhost:2718 after running `just setup`.

## Environment Variables

The setup supports customization via environment variables:

### Database Configuration
- `POSTGRES_USER` (default: postgres)
- `POSTGRES_PASSWORD` (default: postgres)
- `POSTGRES_DB` (default: iceberg_catalog)

### S3/Object Storage Configuration
- `S3_ENDPOINT` (default: http://minio:9000)
- `S3_ACCESS_KEY_ID` (default: test)
- `S3_SECRET_ACCESS_KEY` (default: test)
- `WAREHOUSE_PATH` (default: s3://warehouse/)

### AWS CLI Configuration
- `AWS_ACCESS_KEY_ID` (default: test)
- `AWS_SECRET_ACCESS_KEY` (default: test)
- `AWS_DEFAULT_REGION` (default: us-east-1)
- `AWS_ENDPOINT_URL` (default: http://minio:9000)

## Requirements

- Docker & Docker Compose
- Python 3.10+
- [uv](https://github.com/astral-sh/uv) for dependency management
- [just](https://github.com/casey/just) for task running

## Sample Data

The setup includes NYC For-Hire Vehicle (FHV) trip data from the TLC Trip Record Data. The data is automatically:
1. Uploaded to Minio S3 (`s3://nyc-taxi/`)
2. Loaded into an Iceberg table (`nyc.fhvhv`)
3. Made available for analysis in Marimo notebooks

## Trademarks

Apache Iceberg, Iceberg, Apache, the Apache feather logo, and the Apache Iceberg project logo are either registered trademarks or trademarks of The Apache Software Foundation.
