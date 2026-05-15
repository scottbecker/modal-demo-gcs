import modal
import sys

def main():
    # 1. Connect to the DEPLOYED app functions
    try:
        list_files = modal.Function.from_name("px-container-demo", "list_files")
        run_trans = modal.Function.from_name("px-container-demo", "run_transformation_in_container")
    except modal.Error:
        print("Error: The cluster is not running. Please run ./bin/cluster_start.sh first.")
        sys.exit(1)

    input_dir = "/dataflow_demo_data/input"
    
    print("Querying warm cluster for files...")
    files = list_files.remote(input_dir)
    
    if not files:
        print("No files found.")
        return

    print(f"Triggering parallel processing on warm cluster for {len(files)} files...")
    # This calls the ALREADY WARM instances in the cloud
    for result in run_trans.map(files):
        print(result)

if __name__ == "__main__":
    main()
