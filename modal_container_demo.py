import modal

# 1. Image now only has dependencies
image = modal.Image.debian_slim().pip_install("fastavro")

app = modal.App("px-container-demo")

# 2. Create a Volume for the transformation code
code_volume = modal.Volume.from_name("px-code-volume", create_if_missing=True)

# 3. GCS Configuration
BUCKET_NAME = "dataflow-demo-central-maps"
gcs_secret = modal.Secret.from_name("gcs-hmac-secret")
gcs_mount = modal.CloudBucketMount(
    BUCKET_NAME,
    secret=gcs_secret,
    bucket_endpoint_url="https://storage.googleapis.com",
)

@app.function(
    image=image, 
    volumes={
        "/dataflow_demo_data": gcs_mount,
        "/code": code_volume  # Mount the code volume here
    }, 
    region="us-central",
    timeout=600,
    cpu=2.0,
    min_containers=1
)
def run_transformation_in_container(input_path):
    import subprocess
    import os
    
    output_dir = "/dataflow_demo_data/modal_container_results"
    script_path = "/code/json_to_avro_px.py"
    
    if not os.path.exists(script_path):
        return f"ERROR: Script not found at {script_path}. Please run ./bin/cluster_push_code.sh"

    print(f"Container: Running HOT RELOADED script for {input_path}...")
    
    # Execute the script from the Volume
    result = subprocess.run([
        "python3", script_path,
        input_path,
        "--output_dir", output_dir
    ], capture_output=True, text=True)
    
    if result.returncode == 0:
        print(result.stdout) # Show the script's output in the cloud logs
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
    # This entrypoint is still useful for ephemeral runs
    input_dir = "/dataflow_demo_data/input"
    files = list_files.remote(input_dir)
    for result in run_transformation_in_container.map(files):
        print(result)
