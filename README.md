# Modal GCS File Processing Demo

This repository contains a port of a file processing pipeline to [Modal](https://modal.com), demonstrating parallel execution and Google Cloud Storage (GCS) integration.

## Features
- **Parallel Processing:** Scales out JSON-to-Avro conversion across multiple cloud containers.
- **GCS Integration:** Uses Modal's `CloudBucketMount` to interact directly with GCS buckets.
- **Region Pinning:** Optimizes performance by running compute in the same region as the data (`us-central`).

## Setup

1. **Install Modal:**
   ```bash
   pip install modal
   ```

2. **Authenticate:**
   ```bash
   modal token new
   ```

3. **GCP Secrets:**
   Modal requires HMAC keys for GCS mounting. Create a secret named `gcs-hmac-secret` with:
   - `GOOGLE_ACCESS_KEY_ID`
   - `GOOGLE_ACCESS_KEY_SECRET`

## Running Examples

Execute the scripts in the `bin/` directory:

- **Hello World (Simulation):**
  ```bash
  ./bin/run_hello_world.sh
  ```

- **PX Demo (Real GCS Port):**
  ```bash
  ./bin/run_px_demo.sh
  ```
