#!/bin/bash
# Run the Hello World Modal example
PROJECT_ROOT="$( cd "$( dirname "${BASH_SOURCE[0]}" )/.." &> /dev/null && pwd )"
"$PROJECT_ROOT/.venv/bin/modal" run "$PROJECT_ROOT/hello_world.py"
