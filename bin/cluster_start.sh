#!/bin/bash
# CLUSTER MODE: Start/Deploy the cluster
PROJECT_ROOT="$( cd "$( dirname "${BASH_SOURCE[0]}" )/.." &> /dev/null && pwd )"
echo "Starting/Updating the Warm Cluster (modal deploy)..."
"$PROJECT_ROOT/.venv/bin/modal" deploy "$PROJECT_ROOT/modal_container_demo.py"
echo "Cluster is now warm and ready."
