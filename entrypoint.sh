#!/bin/bash

# sleep infinity
pm2-runtime pm2.config.js &
exec python3.11 -u /app/engine.py