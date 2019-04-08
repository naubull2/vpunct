#!/bin/bash
if [ "$(pgrep -f 'run_vpunct')" ]; then
    sudo kill -9 $(pgrep -f 'run_vpunct')
    echo "vpunct has been terminated." >> ./log/error.log
else
    echo "ERROR: Cannot find run_vpunct daemon." >> ./log/error.log
fi
