#!/bin/bash
# CLUSTER MODE: Start/Deploy the cluster
PROJECT_ROOT="$( cd "$( dirname "${BASH_SOURCE[0]}" )/.." &> /dev/null && pwd )"

echo "Checking if cluster 'px-container-demo' is already running..."
# Look for the app and ensure its state is not 'stopped' using Python
if "$PROJECT_ROOT/.venv/bin/modal" app list --json | "$PROJECT_ROOT/.venv/bin/python3" -c "import sys, json; apps = json.load(sys.stdin); sys.exit(0 if any(app.get('Description') == 'px-container-demo' and app.get('State') != 'stopped' for app in apps) else 1)" > /dev/null 2>&1; then
    echo "Cluster 'px-container-demo' is already deployed and active."
    echo "If you just want to update the code, run: ./bin/cluster_push_code.sh"
    echo "To force a full redeploy, run: modal deploy modal_container_demo.py"
    exit 0
fi

echo "Starting the Warm Cluster (modal deploy)..."
"$PROJECT_ROOT/.venv/bin/modal" deploy "$PROJECT_ROOT/modal_container_demo.py"
echo "Cluster is now warm and ready."
