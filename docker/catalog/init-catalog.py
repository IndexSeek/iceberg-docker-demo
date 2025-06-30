#!/usr/bin/env python3

from pyiceberg.catalog import load_catalog
from pyiceberg.exceptions import (
    ForbiddenError,
    NotInstalledError,
    ServerError,
    UnauthorizedError,
)
import pyarrow as pa
import pyarrow.dataset as ds
import pyarrow.fs as fs
import os

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
        print("Default namespace created successfully!")
        
        # Create NYC namespace for taxi data
        catalog.create_namespace_if_not_exists("nyc")
        print("NYC namespace created successfully!")
        
        # Load NYC taxi data
        print("Loading NYC taxi data...")
        s3 = fs.S3FileSystem(
            access_key=os.environ.get("S3_ACCESS_KEY_ID"),
            secret_key=os.environ.get("S3_SECRET_ACCESS_KEY"),
            endpoint_override=os.environ.get("S3_ENDPOINT"),
            region="us-east-1",
            scheme="http",
        )
        
        dataset = ds.dataset("nyc-taxi/", filesystem=s3, format="parquet")
        
        sch = pa.schema(
            [
                ("hvfhs_license_num", pa.large_string()),
                ("dispatching_base_num", pa.large_string()),
                ("originating_base_num", pa.large_string()),
                ("request_datetime", pa.timestamp("us")),
                ("on_scene_datetime", pa.timestamp("us")),
                ("pickup_datetime", pa.timestamp("us")),
                ("dropoff_datetime", pa.timestamp("us")),
                ("PULocationID", pa.int32()),
                ("DOLocationID", pa.int32()),
                ("trip_miles", pa.float64()),
                ("trip_time", pa.int64()),
                ("base_passenger_fare", pa.float64()),
                ("tolls", pa.float64()),
                ("bcf", pa.float64()),
                ("sales_tax", pa.float64()),
                ("congestion_surcharge", pa.float64()),
                ("airport_fee", pa.float64()),
                ("tips", pa.float64()),
                ("driver_pay", pa.float64()),
                ("shared_request_flag", pa.large_string()),
                ("shared_match_flag", pa.large_string()),
                ("access_a_ride_flag", pa.large_string()),
                ("wav_request_flag", pa.large_string()),
                ("wav_match_flag", pa.large_string()),
                ("cbd_congestion_fee", pa.float64()),
            ]
        )
        
        t = catalog.create_table_if_not_exists(identifier=("nyc", "fhvhv"), schema=sch)
        print("NYC FHVHV table created successfully!")
        
        batch_count = 0
        for batch in dataset.to_batches():
            t.append(pa.Table.from_batches([batch]))
            batch_count += 1
            if batch_count % 10 == 0:
                print(f"Loaded {batch_count} batches...")
        
        print(f"NYC taxi data loading completed! Total batches processed: {batch_count}")
        
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
