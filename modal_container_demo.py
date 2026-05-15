import modal

# 1. Image definition
image = (
    modal.Image.debian_slim()
    .pip_install("fastavro")
    .add_local_file("/home/scott/px_demo/json_to_avro_px.py", "/root/json_to_avro_px.py")
)

app = modal.App("px-container-demo")

# 2. GCS Configuration
BUCKET_NAME = "dataflow-demo-central-maps"
gcs_secret = modal.Secret.from_name("gcs-hmac-secret")
gcs_mount = modal.CloudBucketMount(
    BUCKET_NAME,
    secret=gcs_secret,
    bucket_endpoint_url="https://storage.googleapis.com",
)

@app.function(
    image=image, 
    volumes={"/dataflow_demo_data": gcs_mount}, 
    region="us-central",
    timeout=600,
    cpu=2.0,
    min_containers=1 # This will keep 1 instance warm when DEPLOYED
)
def run_transformation_in_container(input_path):
    import subprocess
    output_dir = "/dataflow_demo_data/modal_container_results"
    
    print(f"Container: Starting transformation for {input_path}...")
    
    result = subprocess.run([
        "python3", "/root/json_to_avro_px.py",
        input_path,
        "--output_dir", output_dir
    ], capture_output=True, text=True)
    
    if result.returncode == 0:
        return f"SUCCESS: {input_path}"
    else:
        return f"ERROR: {input_path}\nStderr: {result.stderr}"

@app.function(image=image, volumes={"/dataflow_demo_data": gcs_mount}, region="us-central")
def list_files(input_dir):
    import os
    if not os.path.exists(input_dir):
        return []
    return [os.path.join(input_dir, f) for f in os.listdir(input_dir) if f.endswith(".json")]

@app.local_entrypoint()
def main():
    input_dir = "/dataflow_demo_data/input"
    print("Listing files...")
    files = list_files.remote(input_dir)
    
    if not files:
        print("No files found.")
        return

    print(f"Processing {len(files)} files...")
    for result in run_transformation_in_container.map(files):
        print(result)
