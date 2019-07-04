#!/bin/bash

set -e

function docker-ip() {
  docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' $1
}

ELASTIC_IP=$(docker-ip "cim_es-master")

echo "Creating index template for elasticsearch instance@${ELASTIC_IP}:9200"

curl -XPOST "${ELASTIC_IP}:9200/_template/honeygrove" --header "Content-Type: application/json" \
    -d @"index_template.json"

echo "\nIndex Template successfully installed!"
