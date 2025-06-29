#!/usr/bin/env python3

import os
import pyarrow as pa
from pyiceberg.catalog.sql import SqlCatalog

# Database configuration
DB_USER = os.getenv("POSTGRES_USER", "postgres")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")
DB_HOST = os.getenv("POSTGRES_HOST", "localhost")
DB_PORT = os.getenv("POSTGRES_PORT", "5432")
DB_NAME = os.getenv("POSTGRES_DB", "iceberg_catalog")

# S3 configuration
S3_ENDPOINT = os.getenv("S3_ENDPOINT", "http://localhost:4566")
S3_ACCESS_KEY = os.getenv("S3_ACCESS_KEY_ID", "test")
S3_SECRET_KEY = os.getenv("S3_SECRET_ACCESS_KEY", "test")
WAREHOUSE_PATH = os.getenv("WAREHOUSE_PATH", "s3://warehouse/")


def main():
    print("Connecting to PyIceberg with SQL catalog...")

    catalog = SqlCatalog(
        name="iceberg_catalog",
        uri=f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}",
        warehouse=WAREHOUSE_PATH,
        init_catalog_tables="false",
        **{
            "s3.endpoint": S3_ENDPOINT,
            "s3.access-key-id": S3_ACCESS_KEY,
            "s3.secret-access-key": S3_SECRET_KEY,
            "s3.path-style-access": "true",
        },
    )

    print("Connected to catalog!")
    print(f"Catalog name: {catalog.name}")

    try:
        namespaces = list(catalog.list_namespaces())
        print(f"Namespaces: {namespaces}")
    except Exception as e:
        print(f"Error listing namespaces: {e}")

    catalog.create_namespace_if_not_exists("default")
    t = pa.table(dict(id=[1, 2, 3], programming_language=["Python", "Rust", "Go"]))
    prog_lang_table = catalog.create_table_if_not_exists(
        "default.programming_language", schema=t.schema
    )
    print(f"Table created: {prog_lang_table.name}")
    prog_lang_table.append(t)
    print("Data appended to table.")
    loaded_table = catalog.load_table("default.programming_language")
    print(f"Loaded table: {loaded_table.name}")
    print(loaded_table.scan().to_arrow())


if __name__ == "__main__":
    main()
