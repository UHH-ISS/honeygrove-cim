#!/bin/sh

if [ "$(id -u)" != "0" ]; then
   echo "Starting the EK stack requires root permissions"
   exit 1
fi

echo "Rising the maximum memory that virtual machines are allowed to map"
sysctl -w vm.max_map_count=262144

echo "Starting database..."
docker-compose -f database/docker-compose.yml up --build
