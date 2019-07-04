#!/bin/bash

if [ "$(id -u)" != "0" ]; then
   echo "[ERR] Starting the honeygrove CIM requires root permissions"
   exit 1
fi

set -eo pipefail

echo "[1] Rising the maximum memory that virtual machines are allowed to map.."
sysctl -w vm.max_map_count=262144

echo "[2] Preparing containers, network and volumes.."
docker pull uhhiss/honeygrove-adapter:latest
docker-compose up --build --no-start

echo "[3] Starting Elasticsearch.."
docker-compose start es-master es-data

echo "[4] Waiting for Elasticsearch setup to finish (30sec).."
sleep 30

echo "[5] Starting Kibana and the honeygrove-adapter.."
docker-compose start kibana adapter

echo "[SUCCESS] Your honeygrove CIM is up and running!"
echo "You may want to run ./prepare_elasticsearch.sh to setup your elasticsearch index template"
