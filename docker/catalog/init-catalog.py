#!/usr/bin/env python3

from pyiceberg.catalog import load_catalog
from pyiceberg.exceptions import (
    NoSuchNamespaceError,
    NamespaceAlreadyExistsError,
    NoSuchTableError,
    TableAlreadyExistsError,
    ValidationError,
    CommitFailedException,
    UnauthorizedError,
    ForbiddenError,
    ServerError,
    NotInstalledError,
)
import pyarrow as pa

try:
    catalog = load_catalog("default")
    print("Catalog tables created successfully!")

    try:
        namespaces = list(catalog.list_namespaces())
        print(f"Namespaces: {namespaces}")
    except (UnauthorizedError, ForbiddenError) as e:
        print(f"Permission error listing namespaces: {e}")
    except ServerError as e:
        print(f"Server error listing namespaces: {e}")
    except Exception as e:
        print(f"Unexpected error listing namespaces: {e}")
    try:
        catalog.create_namespace_if_not_exists("default")
    except (UnauthorizedError, ForbiddenError) as e:
        print(f"Permission error creating namespace: {e}")
        raise
    except NamespaceAlreadyExistsError as e:
        print(f"Namespace already exists: {e}")
    t = pa.table(dict(id=[1, 2, 3], programming_language=["Python", "Rust", "Go"]))
    try:
        prog_lang_table = catalog.create_table_if_not_exists(
            "default.programming_language", schema=t.schema
        )
        print(f"Table created: {prog_lang_table.name}")
    except NoSuchNamespaceError as e:
        print(f"Namespace not found for table creation: {e}")
        raise
    except ValidationError as e:
        print(f"Schema validation error: {e}")
        raise
    except TableAlreadyExistsError as e:
        print(f"Table already exists: {e}")
    try:
        prog_lang_table.append(t)
        print("Data appended to table.")
    except ValidationError as e:
        print(f"Data validation error during append: {e}")
        raise
    except CommitFailedException as e:
        print(f"Failed to commit data append: {e}")
        raise
    try:
        loaded_table = catalog.load_table("default.programming_language")
        print(f"Loaded table: {loaded_table.name}")
    except NoSuchTableError as e:
        print(f"Table not found: {e}")
        raise

    try:
        print(loaded_table.scan().to_arrow())
    except ValidationError as e:
        print(f"Schema validation error during scan: {e}")
        raise
    except Exception as e:
        print(f"Error reading table data: {e}")
        raise
except NotInstalledError as e:
    print(f"Missing required dependencies: {e}")
    raise
except (UnauthorizedError, ForbiddenError) as e:
    print(f"Authentication/permission error: {e}")
    raise
except ServerError as e:
    print(f"Catalog server error: {e}")
    raise
except Exception as e:
    print(f"Unexpected error creating catalog tables: {e}")
    raise
