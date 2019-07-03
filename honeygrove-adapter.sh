#!/bin/bash

echo "Starting honeygrove-adapter"
cd "$(dirname "$0")"
python3 -m honeygrove_adapter "$@"
