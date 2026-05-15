#!/bin/bash
# CLUSTER MODE: Run a job on the warm cluster
PROJECT_ROOT="$( cd "$( dirname "${BASH_SOURCE[0]}" )/.." &> /dev/null && pwd )"
echo "Running job on Warm Cluster..."
"$PROJECT_ROOT/.venv/bin/python3" "$PROJECT_ROOT/cluster_client.py"
