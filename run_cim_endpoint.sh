#!/bin/bash

echo "Starting CIM Endpoint..."
cd "$(dirname "$0")"
python3 -m cim_broker "$@"
