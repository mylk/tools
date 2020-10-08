#!/bin/bash

source secrets.sh

curl -X POST -H "Content-Type: application/json" -H "Authorization: Bearer $DIGITAL_OCEAN_API_KEY" -d '{"type":"power_cycle"}' "https://api.digitalocean.com/v2/droplets/$DIGITAL_OCEAN_DROPLET_ID/actions" -s | jq

