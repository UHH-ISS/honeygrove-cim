#!/bin/sh

if [ "$(id -u)" != "0" ]; then
   echo "Starting the EK stack requires root permissions"
   exit 1
fi

echo "Rising the maximum memory that virtual machines are allowed to map"
sysctl -w vm.max_map_count=262144

echo "Starting EK-Stack..."
docker-compose -f ek_stack/docker-compose.yml up --build
