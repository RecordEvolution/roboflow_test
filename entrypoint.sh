#!/bin/bash

# sleep infinity
pm2-runtime pm2.config.js &
sleep 5
exec python3 -u /app/engine.py