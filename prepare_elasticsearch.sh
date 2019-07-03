#!/bin/bash

echo "Create index template and start Mattermost watcher alerts if enabled"
cd "$(dirname "$0")"
python3 -m honeygrove_adapter.es "$@"
