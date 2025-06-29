#!/usr/bin/env python3

from pyiceberg.catalog import load_catalog
from pyiceberg.exceptions import (
    UnauthorizedError,
    ForbiddenError,
    ServerError,
    NotInstalledError,
)

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
