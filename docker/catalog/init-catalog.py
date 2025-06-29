#!/usr/bin/env python3

from pyiceberg.catalog import load_catalog

catalog = load_catalog("default")

catalog.create_tables()
print("Catalog tables created successfully!")
