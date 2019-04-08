#!/bin/bash
if [ -d "./log" ]; then
    echo "Start logging vpunct API at ./log/error.log..."
else
    mkdir log
    echo "Creating log directory"
fi
python run_vpunct.py --worker 10 > /dev/null 2> ./log/error.log &
