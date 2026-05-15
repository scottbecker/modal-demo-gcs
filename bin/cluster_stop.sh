#!/bin/bash
# CLUSTER MODE: Stop/Undeploy the cluster
PROJECT_ROOT="$( cd "$( dirname "${BASH_SOURCE[0]}" )/.." &> /dev/null && pwd )"
echo "Stopping the Warm Cluster (modal app stop)..."
"$PROJECT_ROOT/.venv/bin/modal" app stop -y px-container-demo
echo "Cluster stopped."
