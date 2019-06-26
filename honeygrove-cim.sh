#!/bin/bash

echo "Starting CIM Endpoint..."
cd "$(dirname "$0")"
python3 -m honeygrove_cim "$@"
