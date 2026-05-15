#!/bin/bash
# Run the Containerized Modal example (using Sandbox)
PROJECT_ROOT="$( cd "$( dirname "${BASH_SOURCE[0]}" )/.." &> /dev/null && pwd )"
"$PROJECT_ROOT/.venv/bin/modal" run "$PROJECT_ROOT/modal_container_demo.py"
