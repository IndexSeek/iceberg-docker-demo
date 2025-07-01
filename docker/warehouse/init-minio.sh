#!/bin/bash

# Configure mc client with Minio server
mc alias set minio $MINIO_ENDPOINT $MINIO_ROOT_USER $MINIO_ROOT_PASSWORD

# Create warehouse bucket
mc mb minio/warehouse

echo "Iceberg bucket creation completed!"

# Create NYC taxi bucket
mc mb minio/nyc-taxi

echo "NYC Taxi bucket creation completed!"

# Upload data files to the nyc-taxi bucket
for file in /data/*.parquet; do
    if [ -f "$file" ]; then
        filename=$(basename "$file")
        echo "Uploading $filename to minio/nyc-taxi/"
        mc cp "$file" "minio/nyc-taxi/$filename"
    fi
done

echo "Data upload to minio/nyc-taxi/ completed!"