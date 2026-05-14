import modal
import os
import time

# Define the image
image = modal.Image.debian_slim().pip_install("fastavro")

app = modal.App("px-demo-modal")

# GCS Configuration - Aligned with px.yaml
BUCKET_NAME = "dataflow-demo-central-maps"
# Modal GCS mount requires HMAC keys in a secret
gcs_secret = modal.Secret.from_name("gcs-hmac-secret")

# CloudBucketMount uses S3-compatible XML API for GCS
gcs_mount = modal.CloudBucketMount(
    BUCKET_NAME,
    secret=gcs_secret,
    bucket_endpoint_url="https://storage.googleapis.com",
)

AVRO_SCHEMA = {
    "type": "record",
    "name": "LogRecord",
    "fields": [
        {"name": "timestamp", "type": "string"},
        {"name": "level", "type": "string"},
        {"name": "message", "type": "string"},
        {"name": "user_id", "type": "int"},
        {"name": "ip_address", "type": "string"}
    ]
}

@app.function(
    image=image, 
    volumes={"/dataflow_demo_data": gcs_mount}, 
    region="us-central",
    timeout=60
)
def list_files(input_dir):
    import os
    print(f"Listing files in {input_dir}...")
    if not os.path.exists(input_dir):
        print(f"Path {input_dir} does not exist.")
        return []
    
    files = [os.path.join(input_dir, f) for f in os.listdir(input_dir) if f.endswith(".json")]
    print(f"Found {len(files)} files.")
    return files

@app.function(
    image=image, 
    volumes={"/dataflow_demo_data": gcs_mount}, 
    region="us-central",
    timeout=300
)
def process_file_modal(input_path):
    import json
    import fastavro
    import os
    
    # Output to a specific subdirectory to avoid clashing with other demos
    output_dir = "/dataflow_demo_data/modal_avro_results"
    os.makedirs(output_dir, exist_ok=True)
    
    base_name = os.path.basename(input_path)
    file_name_no_ext = os.path.splitext(base_name)[0]
    output_path = os.path.join(output_dir, f"{file_name_no_ext}.avro")
    
    print(f"Processing {input_path} -> {output_path}")
    
    records = []
    try:
        with open(input_path, 'r') as f:
            for line in f:
                if line.strip():
                    records.append(json.loads(line))
        
        with open(output_path, 'wb') as out:
            fastavro.writer(out, AVRO_SCHEMA, records)
        
        return f"Successfully processed {input_path}"
    except Exception as e:
        return f"Error processing {input_path}: {e}"

@app.local_entrypoint()
def main():
    input_dir = "/dataflow_demo_data/input"
    
    print(f"Fetching file list from GCS mount (Bucket: {BUCKET_NAME})...")
    try:
        files = list_files.remote(input_dir)
    except Exception as e:
        print(f"Failed to list files: {e}")
        return
    
    if not files:
        print(f"No files found in {input_dir}.")
        return

    print(f"Found {len(files)} files. Starting parallel processing...")
    results = list(process_file_modal.map(files))
    
    for r in results:
        print(r)
