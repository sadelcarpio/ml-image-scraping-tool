#!/bin/bash

# Start the Scrapyd service in the background and log to file
scrapyd > scrapyd.log 2>&1 &

# Give Scrapyd some time to start
sleep 10

# Run scrapyd-deploy
scrapyd-deploy docker

# Tail the logs to hold foreground
tail -f scrapyd.log