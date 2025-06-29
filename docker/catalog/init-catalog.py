#!/usr/bin/env python3

import os
from pyiceberg.catalog.sql import SqlCatalog

# Database configuration
DB_USER = os.getenv("POSTGRES_USER", "postgres")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")
DB_HOST = os.getenv("POSTGRES_HOST", "postgres")
DB_PORT = os.getenv("POSTGRES_PORT", "5432")
DB_NAME = os.getenv("POSTGRES_DB", "iceberg_catalog")

# S3 configuration
S3_ENDPOINT = os.getenv("S3_ENDPOINT", "http://localstack:4566")
S3_ACCESS_KEY = os.getenv("S3_ACCESS_KEY_ID", "test")
S3_SECRET_KEY = os.getenv("S3_SECRET_ACCESS_KEY", "test")
WAREHOUSE_PATH = os.getenv("WAREHOUSE_PATH", "s3://warehouse/")

catalog = SqlCatalog(
    name="iceberg_catalog",
    uri=f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}",
    warehouse=WAREHOUSE_PATH,
    **{
        "s3.endpoint": S3_ENDPOINT,
        "s3.access-key-id": S3_ACCESS_KEY,
        "s3.secret-access-key": S3_SECRET_KEY,
        "s3.path-style-access": "true",
    },
)

catalog.create_tables()
print("Catalog tables created successfully!")
