#!/bin/bash

echo "Creating Mapping and starting Mattermost watcher alerts"
cd "$(dirname "$0")"
python3 -m cim_broker.es "$@"
