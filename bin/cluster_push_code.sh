#!/bin/bash
# CLUSTER MODE: Update the code in the volume (Hot Reload)
PROJECT_ROOT="$( cd "$( dirname "${BASH_SOURCE[0]}" )/.." &> /dev/null && pwd )"
echo "Pushing fresh code to the Warm Cluster volume..."

# Use modal volume put to upload the script with --force to overwrite
"$PROJECT_ROOT/.venv/bin/modal" volume put -f px-code-volume "/home/scott/px_demo/json_to_avro_px.py" "json_to_avro_px.py"

echo "Code updated! Warm containers will use the new logic on their next run."
