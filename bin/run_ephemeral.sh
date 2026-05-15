#!/bin/bash
# EPHEMERAL MODE: Run once and exit
PROJECT_ROOT="$( cd "$( dirname "${BASH_SOURCE[0]}" )/.." &> /dev/null && pwd )"
echo "Running in Ephemeral Mode (one-off app)..."
"$PROJECT_ROOT/.venv/bin/modal" run "$PROJECT_ROOT/modal_container_demo.py"
