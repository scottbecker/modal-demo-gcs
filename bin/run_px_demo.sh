#!/bin/bash
# Run the PX Demo Modal example
PROJECT_ROOT="$( cd "$( dirname "${BASH_SOURCE[0]}" )/.." &> /dev/null && pwd )"
"$PROJECT_ROOT/.venv/bin/modal" run "$PROJECT_ROOT/modal_px_demo.py"
