#!/bin/bash

# sleep infinity
pm2-runtime pm2.config.js &

while true; do
    status_code=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:9001)
    if [ $status_code -eq 200 ]; then
        echo "Successful curl call"
        break
    else
        echo "Failed curl call, sleeping for 1 seconds"
        sleep 1
    fi
done

exec python3.11 -u /app/engine.py