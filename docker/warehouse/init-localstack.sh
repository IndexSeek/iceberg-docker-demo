#!/bin/bash

aws s3 mb s3://warehouse

echo "Iceberg bucket creation completed!"

aws s3 mb s3://nyc-taxi

echo "NYC Taxi bucket creation completed!"

for file in /data/*.parquet; do
    if [ -f "$file" ]; then
        filename=$(basename "$file")
        echo "Uploading $filename to s3://nyc-taxi/"
        aws s3 cp "$file" "s3://nyc-taxi/$filename"
    fi
done

echo "Data upload to s3://nyc-taxi/ completed!"
