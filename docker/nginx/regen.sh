#!/usr/bin/env bash

readonly CONFIG_PATH="/ota/config/conf.json"
readonly SERVER_IP=$(jq -r '.server_ip' $CONFIG_PATH)

> /var/www/html/fw/manifest.json
python3 /ota/scripts/manifest.py -d /firmwares -s ${SERVER_IP} -o /var/www/html/fw/manifest.json

inotifywait -m -e delete,create,modify,moved_to,moved_from /firmwares \
	| while read directory action file; do
		ls /firmwares/; date; echo; # ide kell a generator - manifest.py
		python3 /ota/scripts/manifest.py -d /firmwares -s ${SERVER_IP} -o /var/www/html/fw/manifest.json
	done
