#!/usr/bin/env python3

from pyiceberg.catalog import load_catalog
import pyarrow as pa

try:
    catalog = load_catalog("default")
    print("Catalog tables created successfully!")

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
except Exception as e:
    print(f"Error creating catalog tables: {e}")
    raise
