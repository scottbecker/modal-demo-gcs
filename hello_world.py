import modal
import time

app = modal.App("hello-world")

@app.function()
def process_file(filename):
    print(f"Processing {filename}...")
    # Fake processing time
    time.sleep(2)
    return f"Result for {filename}: {len(filename) * 10} words processed"

@app.local_entrypoint()
def main():
    filenames = [f"file_{i}.txt" for i in range(1, 11)]
    
    print(f"Starting to process {len(filenames)} files...")
    start_time = time.time()
    
    # Use .map() to process files in parallel in the cloud
    for result in process_file.map(filenames):
        print(result)
        
    duration = time.time() - start_time
    print(f"Finished processing in {duration:.2f} seconds.")
