import marimo

__generated_with = "0.14.9"
app = marimo.App(width="medium")


@app.cell
def _():
    import os

    import duckdb
    from pyiceberg.catalog import load_catalog

    catalog = load_catalog("default")
    return catalog, duckdb, os


@app.cell
def _(catalog):
    catalog.list_namespaces()
    return


@app.cell
def _(catalog):
    catalog.list_tables(namespace="nyc")
    return


@app.cell
def _(catalog):
    fhvhv = catalog.load_table(("nyc.fhvhv"))
    return (fhvhv,)


@app.cell
def _(fhvhv):
    fhvhv.scan(limit=100).to_arrow()
    return


@app.cell
def _(duckdb, os):
    con = duckdb.connect(database=":memory:", read_only=False)

    con.load_extension("iceberg")
    con.install_extension("httpfs")
    con.load_extension("httpfs")

    s3_endpoint = os.environ.get("S3_ENDPOINT", "http://minio:9000").replace(
        "http://", ""
    )
    aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID", "minioadmin")
    aws_secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY", "minioadmin123")
    aws_region = os.environ.get("AWS_DEFAULT_REGION", "us-east-1")

    con.sql(f"""CREATE OR REPLACE SECRET (
    type 's3',
    REGION '{aws_region}',
    URL_STYLE 'path',
    ENDPOINT '{s3_endpoint}',
    KEY_ID '{aws_access_key_id}',
    SECRET '{aws_secret_access_key}',
    USE_SSL false
    );""")

    con.sql("SET unsafe_enable_version_guessing = true;")

    result = con.sql(
        "SELECT count(*) FROM iceberg_scan('s3://warehouse/nyc.db/fhvhv');"
    )
    print(result.fetchall())
    return


if __name__ == "__main__":
    app.run()
