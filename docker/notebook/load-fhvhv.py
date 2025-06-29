from pyiceberg.catalog import load_catalog
import pyarrow as pa
import pyarrow.dataset as ds
import pyarrow.fs as fs
import os


catalog = load_catalog("default")

catalog.create_namespace_if_not_exists("nyc")

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

for batch in dataset.to_batches():
    t.append(pa.Table.from_batches([batch]))
